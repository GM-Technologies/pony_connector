from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create default users to database'

    def handle(self, *args, **options):
        default_users = [{'pk': 1, 'username': 'apiuser', 'password': 'ApiAdmin@321'},
                         {'pk': 2, 'username': 'dbuser', 'password': 'DbAdmin@321'}]
        for default_user in default_users:
            try:
                user, created = User.objects.get_or_create(pk=default_user['pk'],
                                                           username=default_user['username'])
                if created:
                    user.is_superuser = True
                    user.is_staff = True
                    user.set_password(default_user['password'])
                    user.save(update_fields=['is_superuser', 'is_staff', 'password'])
            except BaseException as ex:
                print "User - {0} creation failed with exception: " \
                      "{1}".format(default_user['username'],
                                   ex)
        print 'Default Users creation completed!'
