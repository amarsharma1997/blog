# Generated by Django 2.0.2 on 2018-07-06 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20180703_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.topic'),
            preserve_default=False,
        ),
    ]
