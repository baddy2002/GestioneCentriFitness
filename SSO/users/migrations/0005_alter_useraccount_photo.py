# Generated by Django 5.0.6 on 2024-07-16 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_photo_alter_useraccount_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='photo',
            field=models.OneToOneField(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.photo'),
        ),
    ]