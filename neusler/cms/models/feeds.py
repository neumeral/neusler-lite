from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.models import Page


class RSSFeed(models.Model):
    title = models.CharField(
        _("Feed Title"), max_length=255, help_text=_("Title of Feed"), null=False, blank=False
    )
    slug = AutoSlugField(
        _("Feed Slug"),
        populate_from="title",
        editable=True,
        max_length=255,
        help_text=_(
            "Unique slug for the feed. Will be populated automatically from title. Change only if needed."
        ),
        null=False,
        blank=False,
    )
    description = models.CharField(
        _("Feed Description"),
        max_length=255,
        help_text=_("Description of feed"),
        null=True,
        blank=True,
    )
    link = models.CharField(
        _("Website link"), max_length=255, help_text=_("Link of website"), null=True, blank=True
    )
    author_email = models.EmailField(
        _("Feed author email"),
        max_length=255,
        help_text=_("Email of author"),
        null=True,
        blank=True,
    )
    author_name = models.CharField(
        _("Feed author name"),
        max_length=100,
        help_text=_("Name of author"),
        null=True,
        blank=True,
    )
    author_link = models.URLField(
        _("Feed author link"), max_length=255, help_text=_("Link of author"), null=True, blank=True
    )
    use_images = models.BooleanField(
        _("Use Images in Feed"), help_text=_("Whether or not to use images in Feed"), default=True
    )
    limit = models.IntegerField(_("Max number of items in the feed"), default=20)
    linked_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="rss_feeds",
        help_text=_("Create feeds from the pages that are children / belonging to this page"),
        null=False,
    )

    class Meta:
        verbose_name = _("RSS Feed")
        verbose_name_plural = _("RSS Feeds")

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("link"),
        FieldPanel("description"),
        FieldPanel("use_images"),
        FieldPanel("author_name"),
        FieldPanel("author_email"),
        FieldPanel("author_link"),
        FieldPanel("limit"),
        PageChooserPanel("linked_page", ["neucms.ArticleIndexPage", "neucms.CategoryPage"]),
    ]
