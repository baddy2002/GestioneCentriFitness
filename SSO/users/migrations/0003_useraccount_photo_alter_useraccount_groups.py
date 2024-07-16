# Generated by Django 5.0.6 on 2024-07-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_alter_useraccount_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='photo',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='groups',
            field=models.ManyToManyField(related_name='user_accounts', to='auth.group'),
        ),
    ]
