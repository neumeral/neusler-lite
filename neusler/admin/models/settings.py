from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class GeneralSettings(BaseSetting):
    base_url = models.URLField(
        verbose_name=_("Base URL"),
        max_length=200,
        null=False,
        blank=False,
        help_text=_("The base url for the site."),
    )

    tagline = models.CharField(
        verbose_name=_("Tagline"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The tagline of your organisation."),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        max_length=500,
        null=True,
        blank=True,
        help_text=_("A short description about your organisation."),
    )
    contact_phone = models.CharField(
        verbose_name=_("Phone number"),
        max_length=15,
        null=True,
        blank=True,
        help_text=_("The contact phone number of your organisation."),
    )
    contact_address = models.TextField(
        verbose_name=_("Contact Address"), max_length=255, null=True, blank=True
    )
    contact_email = models.EmailField(
        verbose_name=_("Contact Email"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("The contact email address of your organisation."),
    )
    twitter_link = models.URLField(
        verbose_name=_("Twitter Link"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Paste the link of your organisation's Twitter page."),
    )
    facebook_link = models.URLField(
        verbose_name=_("Facebook Link"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Paste the link of your organisation's Facebook page/account."),
    )
    instagram_link = models.URLField(
        verbose_name=_("Instagram Link"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Paste the link of your organisation's Instagram page."),
    )
    youtube_link = models.URLField(
        verbose_name=_("Youtube Link"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Paste the link of your organisation's Youtube channel."),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("base_url"),
                FieldPanel("tagline"),
                FieldPanel("description"),
            ],
            heading="Site Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_address"),
                FieldPanel("contact_phone"),
                FieldPanel("contact_email"),
            ],
            heading="Contact Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("facebook_link"),
                FieldPanel("twitter_link"),
                FieldPanel("instagram_link"),
                FieldPanel("youtube_link"),
            ],
            heading="Social Media Links",
        ),
    ]
