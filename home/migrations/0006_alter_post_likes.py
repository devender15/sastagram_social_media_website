# Generated by Django 3.2.7 on 2021-09-30 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.CharField(default=0, max_length=999999999999999999999999),
        ),
    ]
