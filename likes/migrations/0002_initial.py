# Generated by Django 5.0.1 on 2024-03-27 06:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0002_initial'),
        ('likes', '0001_initial'),
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comment'),
        ),
        migrations.AddField(
            model_name='postlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
    ]
