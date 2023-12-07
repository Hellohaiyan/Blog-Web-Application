from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_article_content_alter_article_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(blank=True, default='C:\\\\Study\\\\CSC244 DataBase\\\\Project\\\\csc244_project\\\\csc244_project\\\\group9_django\\\\uploads\\\\article_cover_images'),
        ),
        migrations.AlterField(
            model_name='article',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]


