# Generated by Django 3.2.7 on 2021-09-29 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210925_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.TextField(default=''),
        ),
    ]
