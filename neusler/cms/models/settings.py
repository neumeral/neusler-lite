from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon="ab-shield-halved-solid")
class SecuritySettings(BaseSetting):
    """
    Settings for Site Security
    """

    class Meta:
        verbose_name = _("Security")

    disable_copy_paste = models.BooleanField(
        verbose_name=_("Disable Copy-Paste"),
        null=False,
        blank=False,
        default=False,
        help_text=_("When turned on, disables copy paste of article content in web browsers."),
    )

    disable_right_click = models.BooleanField(
        verbose_name=_("Disable Right-Click"),
        null=False,
        blank=False,
        default=False,
        help_text=_("When turned on, disables right-click of article content in web browsers."),
    )

    site_scope = models.BooleanField(
        verbose_name=_("Apply site level"),
        null=False,
        blank=False,
        default=False,
        help_text=_("Whether to apply site wide, or only on article"),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("disable_copy_paste"),
                FieldPanel("disable_right_click"),
                FieldPanel("site_scope"),
            ],
            heading="Content Protection",
        ),
    ]
