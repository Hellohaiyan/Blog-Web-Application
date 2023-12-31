
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='avatar',
            field=models.ImageField(default='user_cover_images/default.png', upload_to='user_cover_images'),
        ),
        migrations.AlterField(
            model_name='userbio',
            name='bio',
            field=models.TextField(default="You haven't included your bio. Click edit to update your profile"),
        ),
    ]
