# Generated by Django 2.0.2 on 2018-07-03 16:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_userdetail_lastvisit'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='lastseen',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 3, 16, 18, 50, 811454, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
