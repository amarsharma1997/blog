# Generated by Django 2.0.2 on 2018-07-06 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
    ]
