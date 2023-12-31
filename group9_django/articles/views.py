from datetime import datetime
import json

from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Article, Comment, Category
from .forms import CommentForm, ArticleForm, ArticleCoverImageForm

from django.core.paginator import Paginator
from django.contrib.auth.models import User


def index(request):

    try:
        articles = Article.objects.all().order_by('-created_at', )
        categories = Category.objects.all()

        paginator = Paginator(articles, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        categories_list = []
        for cat in categories:
            a = Article.objects.filter(category=cat)
            categories_list.append({
                "category":cat,
                "number": len(a)
            })

        data = {
            "articles": page_obj,  # articles,
            "page_obj": page_obj,
            "category_list": {
                "data": categories_list,
                "all": len(articles)
            },
            "featured": articles.first
        }

        return render(request, 'articles/index.html', data)
    except Exception as exc:
        print(exc)
        messages.error(request, "Error fetching list of articles.")
        return render(request, 'articles/index.html', {})




def get_articles_by_category(request, category):

    try:
        category = Category.objects.get(category=category)
        articles = Article.objects.filter(category=category).order_by('-created_at', )
        categories = Category.objects.all()

        all_articles = Article.objects.all().order_by('-created_at', )

        categories_list = []
        for cat in categories:
            a = Article.objects.filter(category=cat)
            categories_list.append({
                "category": cat,
                "number": len(a)
            })

        if articles:
            paginator = Paginator(articles, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            data = {
                "articles": page_obj,  # articles,
                "page_obj": page_obj,
                "category_list": {
                    "data": categories_list,
                    "all": len(Article.objects.all())
                },
                "featured": all_articles.first

            }

            return render(request, 'articles/index.html', data)
        else:

            data = {
                "category_list": {
                    "data": categories_list,
                    "all": len(all_articles)
                },
                "error": True,
                "featured": all_articles.first
            }

            messages.info(request, "No articles found for the selected categories")
            return render(request, 'articles/index.html', data)


    except Exception as exc:
        print(exc)
        messages.error(request, "Articles not found for the selected category")
        return render(request, 'articles/index.html', {"error": True})



def get_user_articles(request, username):

    try:

        user = User.objects.get(username=username)

        articles = Article.objects.filter(created_by=user).order_by('-created_at', )

        all_articles = Article.objects.all().order_by('-created_at', )

        categories = Category.objects.all()


        categories_list = []
        for cat in categories:
            a = Article.objects.filter(category=cat)
            categories_list.append({
                "category": cat,
                "number": len(a)
            })

        if articles:
            paginator = Paginator(articles, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            data = {
                "articles": page_obj,  # articles,
                "page_obj": page_obj,
                "category_list": {
                    "data": categories_list,
                    "all": len(Article.objects.all())
                },
                "featured": all_articles.first

            }

            return render(request, 'articles/index.html', data)
        else:
            data = {
                "category_list": {
                    "data": categories_list,
                    "all": len(all_articles)
                },
                "error": True,
                "featured": all_articles.first
            }

            messages.info(request, "User has not published any article!")
            return render(request, 'articles/index.html', data)


    except Exception as exc:
        messages.error(request, "Error fetching your created articles")
        return render(request, 'articles/index.html', {"error": True})



def get_article(request, article_slug):
    try:
        # Create comment form
        add_comment_form = CommentForm()

        article_cover_image_form = ArticleCoverImageForm()

        selected_article = Article.objects.get(slug=article_slug)
        comments = Comment.objects.filter(article=selected_article).order_by('-created_at',)

        paginator = Paginator(comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'articles/article.html', {
            "title": selected_article.title,
            "subtitle": selected_article.subtitle,
            "content": selected_article.content,
            "slug": selected_article.slug,
            "created_by": selected_article.created_by,
            "created_at": selected_article.created_at,
            "updated_at": selected_article.updated_at,
            "article_found" : True,
            "cover_image" : selected_article.cover_image,
            "comments" : comments,
            "page_obj": page_obj,
            "category" : selected_article.category,
            "add_comment_form": add_comment_form,
            "categories": Category.objects.all(),
            "form": article_cover_image_form
        })

    except Exception as exc:
        print(exc)
        return render(request, 'articles/article.html', {
            "article_found" : False
        })




@login_required(login_url='signin')
def add_article(request):

    if request.method == 'GET':
        article_form = ArticleForm(initial={'category': '1'})
        return render(request, 'articles/add.html', {"form": article_form, 'is_error': False})

    elif request.method == 'POST':
        try:
            article_form = ArticleForm(request.POST, request.FILES)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.created_by = request.user
                article.slug = slugify(article.title)
                article.save()

                messages.success(request, 'Your article is ready')
                return redirect('get-article', article_slug=article.slug)

            else:
                article_form = ArticleForm(initial={'category': '1'})
                return render(request, 'articles/add.html', {"form": article_form, 'is_error': True})

        except Exception as exc:
            print("printing...")
            print(exc)
            article_form = ArticleForm(initial={'category': '1'})
            return render(request, 'articles/add.html', {"form": article_form, 'is_error': True})
    else:
        print("Unknown")



@login_required(login_url='signin')
def edit_article(request, article_slug):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "PUT":
            title = json.loads(request.body)["title"]
            subtitle = json.loads(request.body)["subtitle"]
            content = json.loads(request.body)["content"]
            category_id = json.loads(request.body)["category"]

            try:
                article = Article.objects.get(slug=article_slug)
                category = Category.objects.get(pk=category_id)
                article.title = title
                article.subtitle = subtitle
                article.content = content
                article.category = category
                article.save()

                return JsonResponse({"updated_at": article.updated_at}, status=200)

            except Exception as exc:
                return JsonResponse({"error": "Unable to update article. Please try again later"}, status=400)

        elif request.is_ajax and request.method == "GET":
            try:
                article = Article.objects.get(slug=article_slug)
                return JsonResponse({"title": article.title, "subtitle": article.subtitle, "content" : article.content}, status=200)

            except Exception as exc:
                return JsonResponse({"error": "Unable to cancel edit article. Please try again later"}, status=400)
        else:
            return JsonResponse({"error": "Unknown request error!"}, status=400)
    else:
        messages.info(request, 'You are not signed in. Please Sign in to continue!')
        return redirect('signin')

@login_required(login_url='signin')
def update_article_image(request, article_slug):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "POST":
            try:
                article = Article.objects.get(slug=article_slug)
                form = ArticleCoverImageForm(request.POST, request.FILES, instance=article)
                if form.is_valid():
                    form.save()
                    return JsonResponse({"photo": article.cover_image.url}, status=200)
                else:
                    return JsonResponse({"error": "Unable to update image. Please try again later."}, status=400)
            except Exception as exc:
                print(exc)
                return JsonResponse({"error": "Unable to update image. Please try again later."}, status=400)
        else:
            return JsonResponse({"error": "Unknown request error!"}, status=400)

    else:
        messages.info(request, 'You are not signed in. Please Sign in to continue!')
        return redirect('signin')




@login_required(login_url='signin')
def add_comment(request, article_slug, username):
    if request.is_ajax and request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)

            article = Article.objects.get(slug=article_slug)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)

                user = User.objects.get(username=username)
                comment.created_by = user
                comment.article = article
                comment.save()
                ser_instance = serializers.serialize('json', [comment, ])
                full_name = comment.created_by.first_name + " " + comment.created_by.last_name
                username = comment.created_by.username

                data = {
                    "name": full_name,
                    "username": username,
                }


                return JsonResponse({"comment": ser_instance, "id": comment.comment_id, "user": json.dumps(data)},
                                    status=200)
            else:

                print("Form is Invalid")
                return JsonResponse({"error": comment_form.errors}, status=400)
        else:
            messages.info(request, 'You are not signed in. Please Sign in to continue!')
            return redirect('signin')
    else:
        return JsonResponse({"error": "Unknown request"}, status=400)


@login_required(login_url='signin')
def edit_comment(request, comment_id):
    if request.is_ajax and request.method == "PUT":
        comment_from_ajax = json.loads(request.body)["comment"]

        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.comment = comment_from_ajax
            comment.save()

            return JsonResponse({"updated_at": comment.updated_at}, status=200)

        except Exception as exc:
            return JsonResponse({"error": "Unable to update comment. Please try again later"}, status=400)

    elif request.is_ajax and request.method == "GET":
        try:
            comment = Comment.objects.get(pk=comment_id)
            return JsonResponse({"comment": comment.comment}, status=200)

        except Exception as exc:
            return JsonResponse({"error": "Unable to cancel edit comment. Please try again later"}, status=400)
    else:
        return JsonResponse({"error": "Unknown request"}, status=400)


@login_required(login_url='signin')
def delete_comment(request, comment_id):
    if request.is_ajax and request.method == "DELETE":
        print("comment id is: " + str(comment_id))
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({"message": "deleted"}, status=200)
        except Exception as exc:
            print(exc)
            return JsonResponse({"error": "Could not remove comment. Please try again later!"}, status=400)
    else:
        return JsonResponse({"error": "Unknown request"}, status=400)
