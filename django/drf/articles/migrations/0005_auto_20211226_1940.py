# Generated by Django 3.2.7 on 2021-12-26 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_like_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='like_users',
        ),
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
    ]