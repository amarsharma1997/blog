# Generated by Django 2.0.2 on 2018-07-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_remove_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
