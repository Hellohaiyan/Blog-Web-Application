from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20210707_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.TextField(blank=True, null=True)),
                ('github', models.TextField(blank=True, null=True)),
                ('twitter', models.TextField(blank=True, null=True)),
                ('youtube', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
