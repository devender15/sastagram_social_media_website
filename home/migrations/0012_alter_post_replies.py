# Generated by Django 3.2.7 on 2021-10-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_post_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='replies',
            field=models.TextField(default=''),
        ),
    ]
