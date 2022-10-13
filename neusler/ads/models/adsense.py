from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class GoogleAdsSetting(BaseSetting):
    class Meta:
        verbose_name = _("Google Adsense")

    auto_ads_js = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Auto Ads script"),
        help_text=_("Paste the script snippet generated for auto ads from adsense."),
    )
    auto_ads_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable Auto ads"),
        help_text=_("Enable this button to use auto ads."),
    )
    in_article_ad_js = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("In-article ads script"),
        help_text=_("Paste the script snippet generated for in-article ads from adsense."),
    )
    in_article_ad_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable In-article ads"),
        help_text=_("Enable this button to use in-article ads.(auto ads should be disabled)."),
    )
    sidebar_ad_js = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Sidebar ads script"),
        help_text=_("Paste the script snippet generated for display ads from adsense."),
    )
    sidebar_ad_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable Sidebar ads"),
        help_text=_("Enable this button to use sidebar ads.(auto ads should be disabled)."),
    )

    panels = [
        FieldPanel("auto_ads_js"),
        FieldPanel("auto_ads_enable"),
        FieldPanel("in_article_ad_js"),
        FieldPanel("in_article_ad_enable"),
        FieldPanel("sidebar_ad_js"),
        FieldPanel("sidebar_ad_enable"),
    ]
