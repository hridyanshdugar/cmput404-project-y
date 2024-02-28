# Generated by Django 5.0.2 on 2024-02-28 06:18

import image.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=12312, upload_to=image.models.image_upload_path),
            preserve_default=False,
        ),
    ]
