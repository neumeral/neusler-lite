from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Generate image renditions for Wagtail Images"

    def handle(self, *args, **options):
        from wagtail.images import get_image_model

        ImageModel = get_image_model()
        images = ImageModel.objects.filter(~Q(title__startswith="promo"))
        renditions = ["fill-80x60", "fill-400x300", "fill-480x360", "fill-1200x900", "fill-960x720"]

        for image in images:
            for rendition in renditions:
                print("Processing image -", image.title, rendition)
                image.get_rendition(rendition)
                image.get_rendition(f"{rendition}|format-webp")
