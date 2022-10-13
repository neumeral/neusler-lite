from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

UserModel = get_user_model()


@register_snippet
class Author(models.Model):
    name = models.CharField(_("name"), max_length=50, blank=True)
    designation = models.CharField(_("designation"), max_length=50, blank=True)
    short_bio = models.TextField(_("short bio"), null=True, blank=True, max_length=300)
    photo = models.ImageField(
        _("photo"), upload_to="author_photos/", default="author_photos/default_avatar.png"
    )
    user = models.OneToOneField(
        UserModel, on_delete=models.SET_NULL, related_name="author", null=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("designation"),
        FieldPanel("short_bio"),
        FieldPanel("photo"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class PageSnippet(ClusterableModel):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
        help_text=_(
            "Unique identifier of the section. "
            "Will be populated automatically from title of section. "
            "Change only if needed."
        ),
    )

    class Meta:
        verbose_name = "Page Snippet"
        verbose_name_plural = "Page Snippets"

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ],
            heading=_("Snippet Articles"),
        ),
        InlinePanel("snippet_articles", label=_("Articles in this Snippet")),
    ]

    def __str__(self):
        return self.title


class SnippetArticle(Orderable):
    section = ParentalKey(
        "neucms.PageSnippet",
        related_name="snippet_articles",
        help_text=_("Section to which this article belongs"),
    )
    link_page = models.ForeignKey(
        "neucms.ArticlePage",
        on_delete=models.CASCADE,
        related_name="article_subsection",
        help_text=_("Page to link to "),
    )

    panels = [
        PageChooserPanel("link_page"),
    ]

    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.link_page.title


class PageSection(Orderable):
    section = ParentalKey(
        "neucms.HomePage",
        related_name="page_sections",
        help_text=_("Section to which this article belongs"),
    )
    link_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="page_subsection",
        help_text=_("Page to link to "),
    )

    panels = [
        PageChooserPanel("link_page"),
    ]

    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.link_page.title

    @property
    def title(self):
        return self.link_page.title

    @property
    def articles(self):
        return self.link_page.specific.articles_shortlist


class CategorySection(Orderable):
    section = ParentalKey("neucms.HomePage", related_name="category_sections")
    link_category_page = models.ForeignKey(
        "neucms.CategoryPage",
        on_delete=models.CASCADE,
        related_name="homepage_section",
        help_text="The category to which is to be displayed.",
    )

    panels = [PageChooserPanel("link_category_page")]

    def __str__(self):
        return self.link_category_page.title

    @property
    def articles(self):
        return self.link_category_page.articles_shortlist


@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
        help_text=_(
            "Unique identifier of menu. "
            "Will be populated automatically from title of menu. "
            "Change only if needed."
        ),
    )

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ],
            heading=_("Menu"),
        ),
        InlinePanel("menu_items", label=_("Menu Item")),
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    menu = ParentalKey(
        "neucms.Menu", related_name="menu_items", help_text=_("Menu to which this item belongs")
    )
    title = models.CharField(
        max_length=50, help_text=_("Title of menu item that will be displayed")
    )
    link_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text=_(
            "URL to link to, e.g. /accounts/signup (no language prefix, "
            "LEAVE BLANK if you want to link to a page instead of a URL)"
        ),
    )
    link_page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Page to link to (LEAVE BLANK if you want to link to a URL instead)"),
    )
    if_submenu = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text=_("If this menu item has a submenu. Leave if it does not."),
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    show_when = models.CharField(
        max_length=15,
        choices=[
            ("always", _("Always")),
            ("logged_in", _("When logged in")),
            ("not_logged_in", _("When not logged in")),
        ],
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("if_submenu"),
        ImageChooserPanel("icon"),
        FieldPanel("show_when"),
    ]

    def url(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return None

    @property
    def slug_of_submenu(self):
        if self.if_submenu:
            return slugify(self.title)
        return None

    def show(self, authenticated):
        return (
            (self.show_when == "always")
            or (self.show_when == "logged_in" and authenticated)
            or (self.show_when == "not_logged_in" and not authenticated)
        )

    def __str__(self):
        return self.title


@register_snippet
class FooterSection(ClusterableModel):
    title = models.CharField(_("title"), max_length=50)

    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Sections"

    def __str__(self):
        return self.title

    panels = [FieldPanel("title"), InlinePanel("footer_links", heading="Footer Links")]


class FooterLink(Orderable):
    footer_section = ParentalKey(
        "neucms.FooterSection", null=False, blank=False, related_name="footer_links"
    )
    title = models.CharField(_("title"), max_length=50, help_text=_("Title of the footer item."))
    link_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Page to which the item is linked, leave blank if its a url."),
    )
    link_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("URL to which the item is linked, leave blank if its a page."),
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
    ]

    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
