# Generated by Django 2.1.5 on 2019-03-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default='This is the body this is to check'),
        ),
    ]
