# Generated by Django 3.2.7 on 2021-09-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.CharField(blank=True, max_length=999999999, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.CharField(blank=True, max_length=999999999, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uploaded',
            field=models.CharField(blank=True, max_length=999999999, null=True),
        ),
    ]