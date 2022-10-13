from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

import pytz
from wagtail.models import Page


class Command(BaseCommand):
    help = "Updates published date"

    def handle(self, *args, **options):
        new_publish_time = datetime.now(pytz.utc) - timedelta(days=1)
        for page in Page.objects.all():
            page.last_published_at = new_publish_time
            page.save()
        self.stdout.write(
            self.style.SUCCESS(f"Updated last_published_at to timestamp - {new_publish_time}")
        )
