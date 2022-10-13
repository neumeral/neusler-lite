from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class CategoryPageAd(models.Model):
    ad_title = models.CharField(max_length=50, help_text=_("Title to identify the ad"))
    all_categories = models.BooleanField(
        default=False, help_text=_("Select if the ad is to be displayed on all pages.")
    )
    ad_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    ad_url = models.CharField(
        max_length=500, null=True, blank=True, help_text=_("URL to link the ad to")
    )

    class Meta:
        verbose_name = "Category Page Advertisement"
        verbose_name_plural = "Category Page Ads"

    panels = [
        FieldPanel("ad_title"),
        FieldPanel("all_categories"),
        ImageChooserPanel("ad_image"),
        FieldPanel("ad_url"),
    ]

    def __str__(self):
        return self.ad_title
