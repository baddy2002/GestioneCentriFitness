from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Initialize the database with default groups'

    def handle(self, *args, **kwargs):
        groups = [
            ('customer', 'Customer'),
            ('trainer', 'Trainer'),
            ('nutritionist', 'Nutritionist'),
            ('manager', 'Manager'),
            ('admin', 'Admin'),
        ]

        for name, verbose_name in groups:
            # Usa get_or_create per evitare errori se il gruppo esiste già
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{name}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{name}" already exists.'))
