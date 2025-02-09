# Generated by Django 5.0.1 on 2024-03-27 06:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0002_initial'),
        ('followers', '0002_initial'),
        ('inbox', '0001_initial'),
        ('likes', '0001_initial'),
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='author',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inbox',
            name='comment',
            field=models.ManyToManyField(blank=True, to='comments.comment'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='commentLikes',
            field=models.ManyToManyField(blank=True, to='likes.commentlike'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='followRequest',
            field=models.ManyToManyField(blank=True, to='followers.followstatus'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='post',
            field=models.ManyToManyField(blank=True, to='posts.post'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='postLikes',
            field=models.ManyToManyField(blank=True, to='likes.postlike'),
        ),
    ]
