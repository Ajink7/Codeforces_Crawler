# Generated by Django 2.2.5 on 2020-06-23 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20200623_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]