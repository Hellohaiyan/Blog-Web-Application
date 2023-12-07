from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_alter_article_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='article_cover_images'),
        ),
    ]
