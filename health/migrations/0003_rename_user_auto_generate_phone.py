# Generated by Django 5.1.1 on 2024-09-18 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_auto_generate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auto_generate',
            old_name='user',
            new_name='phone',
        ),
    ]