from django.shortcuts import render, redirect
from .forms import SigninForm, SignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserBio, UserAvatar
from .forms import UserAvatarForm, ChangePasswordForm

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

import json

def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            signup_form = SignupForm()
            return render(request, 'users/signup.html', {"form": signup_form, 'is_error': False})

        elif request.method == 'POST':
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                user = User.objects.get(username=username)
                bio = UserBio(user=user, bio="You haven't included your bio. Click edit to update your profile")
                bio.save()

                avatar = UserAvatar(user=user, avatar="user_cover_images/default.png")
                avatar.save()
                first_name = signup_form.cleaned_data.get('first_name')
                messages.success(request, first_name + ', Your account was successfully created! Please Sign-in to continue.')
                return redirect('signin')

            else:
                return render(request, 'users/signup.html', {"form": signup_form, 'is_error': True})

    else:
        return redirect('all-articles')


def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            signin_form = SigninForm()
            return render(request, 'users/signin.html', {"form": signin_form, 'is_error': False})
        elif request.method == 'POST':
            signin_form = SigninForm(data=request.POST)
            if signin_form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)

                    return redirect('profile', user)
                else:
                    return render(request, 'users/signin.html', {"form": signin_form, 'is_error': True})
            else:
                return render(request, 'users/signin.html', {"form": signin_form, 'is_error': True})
    else:
        return redirect('all-articles')


@login_required(login_url='signin')
def change_password(request, username):
    if request.method == 'GET':
        try:
            form = ChangePasswordForm()
            user = User.objects.get(username=username)
            return render(request, 'users/change_password.html', {
                "user": user,
                "form": form
            })

        except Exception as exc:
            print(exc)
            return render(request, 'users/change_password.html', {
                "user": {}
            })
    elif request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.is_valid():
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change-password', user)

            else:
                messages.error(request, "Your passwords do not match.")
                return redirect('change-password', user)

        except Exception as exc:
            messages.error("Cannot change password. Ensure that your password matches")
            return redirect('change-password', user)



@login_required(login_url='signin')
def sign_out(request):
    messages.success(request, 'You are logged out. Please login to continue.')
    logout(request)
    return redirect('signin')


def profile(request, username):
    avatar_form = UserAvatarForm()


    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            return render(request, 'users/profile.html', {
                "user": user,
                "form": avatar_form,
            
            })

        except Exception as exc:
            print(exc)
            return render(request, 'users/profile.html', {
                "user": {}
            })

    elif request.method == 'POST':
        try:
            user_form = UserAvatarForm(request.POST, request.FILES)
            user = User.objects.get(username=username)
            avatar_form = UserAvatarForm()
            if user_form.is_valid():
                user_avatar_obj = UserAvatar.objects.get(user=request.user)
                user_avatar_obj.avatar = user_form.cleaned_data['avatar']
                user_avatar_obj.save()

                return render(request, 'users/profile.html', {"user": user, "form": avatar_form, "social": social_form})

            else:

                messages.error(request, 'Form is Invalid')
                return render(request, 'users/profile.html', {"form": avatar_form, "user": user})

        except Exception as exc:
            messages.error(request, 'Could not update avatar')
            print(exc)
            return render(request, 'users/profile.html', {"form": avatar_form, "user": user})


    elif request.method == 'PUT' and request.is_ajax:
        first_name = json.loads(request.body)["first_name"]
        last_name = json.loads(request.body)["last_name"]
        bio = json.loads(request.body)["bio"]
        email = json.loads(request.body)["email"]


        try:
            user = User.objects.get(email=email)
            if user == request.user:
                # Get user
                user = User.objects.get(username=username)
                user.first_name = first_name
                user.last_name = last_name

                user.save()

                user_bio = UserBio.objects.get(user=user)
                user_bio.bio = bio
                user_bio.save()

            else:
                return JsonResponse({"error": "Email already exist for a different account. Please select another email"}, status=400)

        except Exception as exc:
            return JsonResponse({"error": "Unable to update user. Please try again later"}, status=400)

    return render(request, 'users/profile.html')


def edit_profile(request, username):
    if request.method == 'GET' and request.is_ajax:
        try:
            user = User.objects.get(username=username)

            user_bio = user.userbio.bio
            return JsonResponse({"first_name": user.first_name, "last_name": user.last_name, "bio": user_bio, "email": user.email},status=200)

        except Exception as exc:
            return JsonResponse({"error": "Unable to cancel update profile. Please try again later"}, status=400)

        




