# Generated by Django 2.0.2 on 2018-07-24 16:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20180724_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='recently_searched_tags',
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='lastseen',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 16, 10, 29, 707248, tzinfo=utc)),
        ),
    ]
