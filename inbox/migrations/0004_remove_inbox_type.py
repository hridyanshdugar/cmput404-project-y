# Generated by Django 5.0.1 on 2024-04-06 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0003_remove_inbox_commentlikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbox',
            name='type',
        ),
    ]
