# Generated by Django 5.0.1 on 2024-03-10 07:22

import users.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('global_id', models.CharField(default=uuid.uuid4, max_length=300, unique=True)),
                ('url', models.TextField(blank=True, default='')),
                ('host', models.TextField(blank=True, default='')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('profileImage', models.ImageField(null=True, upload_to=users.models.pfp_upload_path)),
                ('profileBackgroundImage', models.ImageField(null=True, upload_to=users.models.profilebackground_upload_path)),
                ('github', models.TextField(blank=True, default='')),
                ('displayName', models.TextField(blank=True, default='')),
                ('approved', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
