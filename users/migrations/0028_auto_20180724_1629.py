# Generated by Django 2.0.2 on 2018-07-24 16:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_auto_20180724_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='lastseen',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 16, 29, 30, 590027, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='recently_searched_tags',
            field=models.TextField(blank=True, default='', max_length=5000),
            preserve_default=False,
        ),
    ]
