# Generated by Django 2.2.5 on 2020-05-11 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_email_max_length'),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0004_auto_20200511_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
