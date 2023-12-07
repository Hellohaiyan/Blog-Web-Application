
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210714_1611'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSocial',
        ),
    ]
