from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(blank=True, default='article_cover_images/article_cover_default.png', null=True, upload_to='article_cover_images'),
        ),
    ]
