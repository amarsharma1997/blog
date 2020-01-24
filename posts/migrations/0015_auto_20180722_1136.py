# Generated by Django 2.0.2 on 2018-07-22 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20180707_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentthread',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
    ]