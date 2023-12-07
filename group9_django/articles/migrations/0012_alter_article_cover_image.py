
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_alter_article_cover_image_alter_article_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(upload_to='article_cover_images'),
        ),
    ]
