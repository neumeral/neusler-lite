from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon="ax-google-analytics")
class AnalyticsSettings(BaseSetting):
    """
    Tracking and Google Analytics.

    Note:
    - AnalyticsSettings is part of Wagtail CRX (CodeRed Extensions)
    - Source: https://github.com/coderedcorp/coderedcms
    - License: https://github.com/coderedcorp/coderedcms/blob/aec431be55a8a04f179ac4e7ec88d469c2856856/LICENSE

    """

    class Meta:
        verbose_name = _("Google Tracking")

    ga_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("UA Tracking ID"),
        help_text=_('Your Google "Universal Analytics" tracking ID (begins with "UA-")'),
    )
    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Google Tracking ID"),
        help_text=_('Your Google Analytics 4 tracking ID (begins with "G-")'),
    )
    ga_track_button_clicks = models.BooleanField(
        default=False,
        verbose_name=_("Track button clicks"),
        help_text=_(
            "Track all button clicks using Google Analytics event tracking. "
            "Event tracking details can be specified in each button’s advanced "
            "settings options."
        ),
    )
    gtm_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Google Tag Manager ID"),
        help_text=_('Begins with "GTM-"'),
    )
    head_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("<head> tracking scripts"),
        help_text=_("Add tracking scripts between the <head> tags."),
    )
    body_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("<body> tracking scripts"),
        help_text=_("Add tracking scripts toward closing <body> tag."),
    )

    panels = [
        HelpPanel(
            heading=_("Know your tracking"),
            content=_(
                "<h2>Which tracking IDs do I need?</h2>"
                "<p>Before adding tracking to your site, "
                '<a href="https://docs.coderedcorp.com/wagtail-crx/how_to/add_tracking_scripts.html" '  # noqa
                'target="_blank">read about the difference between G, UA, GTM, '
                "and other tracking IDs</a>.</p>"
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel("ga_g_tracking_id"),
                FieldPanel("ga_tracking_id"),
                FieldPanel("ga_track_button_clicks"),
            ],
            heading=_("Google Analytics"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("gtm_id"),
            ],
            heading=_("Google Tag Manager"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("head_scripts"),
                FieldPanel("body_scripts"),
            ],
            heading=_("Other Tracking Scripts"),
        ),
    ]
