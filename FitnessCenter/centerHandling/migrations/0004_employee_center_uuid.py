# Generated by Django 5.0.7 on 2024-07-21 15:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centerHandling', '0003_alter_center_manager_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='center_uuid',
            field=models.CharField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]