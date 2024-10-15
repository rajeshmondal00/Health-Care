# Generated by Django 5.1.1 on 2024-10-15 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0012_register_user_gender_register_user_user_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register_user',
            name='email',
        ),
        migrations.AddField(
            model_name='register_user',
            name='id',
            field=models.BigAutoField(auto_created=True, default=123456, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register_user',
            name='user',
            field=models.OneToOneField(default=123456, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
