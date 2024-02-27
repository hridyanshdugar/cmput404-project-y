# Generated by Django 5.0.2 on 2024-02-27 05:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('global_id', models.CharField(max_length=300, unique=True)),
                ('source', models.URLField(max_length=300)),
                ('origin', models.URLField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
                ('contentType', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FRIENDS', 'FRIENDS'), ('UNLISTED', 'UNLISTED')], default='PUBLIC', max_length=8)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
