# Generated by Django 5.1.1 on 2024-10-03 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0008_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='email',
            field=models.ForeignKey(default="rajeshmondalmain@gmail.com", on_delete=django.db.models.deletion.CASCADE, to='health.register_user'),
            preserve_default=False,
        ),
    ]