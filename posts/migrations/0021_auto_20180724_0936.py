# Generated by Django 2.0.2 on 2018-07-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_auto_20180724_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='topic',
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ManyToManyField(to='posts.topic'),
        ),
    ]