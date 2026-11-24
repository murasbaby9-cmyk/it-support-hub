import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
        if not password: return
        if len(password)<12: raise CommandError('Admin password must have at least 12 characters')
        user,created=get_user_model().objects.get_or_create(username=os.getenv('DJANGO_SUPERUSER_USERNAME','muras'))
        user.is_staff=True; user.is_superuser=True; user.is_active=True
        if not user.check_password(password): user.set_password(password)
        user.save()
        self.stdout.write('Administrator ready')
