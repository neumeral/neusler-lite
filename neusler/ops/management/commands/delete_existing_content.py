from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from wagtail.models import Page


class Command(BaseCommand):
    help = "Deletes existing content_types and django_auth"

    def handle(self, *args, **options):
        Page.objects.all().delete()
        ContentType.objects.all().delete()
        Permission.objects.all().delete()
