# Generated by Django 5.1.4 on 2025-01-05 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_aboutcart_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='additional_info_location',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='district',
        ),
    ]
