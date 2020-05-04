from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    help = 'Creates a default administrator account.'

    def handle(self, *args, **options):
        if User.objects.count() == 0:

            self.stdout.write('Creating default user and admin accounts for testing.')
            user = User.objects.create_user('alice', 'alice@example.com', 'password')
            user = User.objects.create_user('bob', 'bob@example.com', 'password')

            user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
            user.is_admin = True
            user.is_staff = True
            user.save()

            # username = 'admin'
            # email = 'admin@example.com'
            # password = 'admin'
            # admin = Account.objects.create_superuser(email=email, username=username, password=password)
            # admin.is_active = True
            # admin.is_admin = True
            # admin.save()