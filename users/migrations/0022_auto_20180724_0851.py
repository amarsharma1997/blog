# Generated by Django 2.0.2 on 2018-07-24 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20180723_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='lastseen',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 8, 50, 56, 342846, tzinfo=utc)),
        ),
    ]
