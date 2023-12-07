
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210714_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocial',
            name='github',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='linkedin',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='twitter',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='youtube',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
