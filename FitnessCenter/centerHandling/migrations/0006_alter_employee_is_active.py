# Generated by Django 5.0.7 on 2024-07-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centerHandling', '0005_employee_user_uuid_alter_exit_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
