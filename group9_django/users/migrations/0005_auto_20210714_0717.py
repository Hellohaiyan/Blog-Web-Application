from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usersocial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocial',
            name='github',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='linkedin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='twitter',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='youtube',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
