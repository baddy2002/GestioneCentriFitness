# Generated by Django 5.0.6 on 2024-07-12 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_accounts', to='auth.group'),
        ),
    ]
