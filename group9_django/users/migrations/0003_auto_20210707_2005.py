from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210707_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='avatar',
            field=models.ImageField(upload_to='user_cover_images'),
        ),
        migrations.AlterField(
            model_name='userbio',
            name='bio',
            field=models.TextField(),
        ),
    ]
