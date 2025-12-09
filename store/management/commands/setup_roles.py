from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Setup Admin and StoreOfficer roles"

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        officer_group, _ = Group.objects.get_or_create(name='StoreOfficer')

        # Assign permissions to StoreOfficer (CRUD items)
        perms = Permission.objects.filter(
            content_type__app_label='store',
            codename__in=['add_item', 'view_item', 'change_item', 'delete_item']
        )

        officer_group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS("Roles created successfully!"))

