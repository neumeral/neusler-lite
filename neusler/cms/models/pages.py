from datetime import date, datetime, timedelta

from django.apps import apps
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_comments_xtd.models import XtdComment
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.api import APIField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailseo.models import SeoMixin, SeoType, TwitterCard


from ..blocks import (
    HTMLEmbedBlock,
    InArticleGoogleAdBlock,
    InlineCarousalBlock,
    InlineImageBlock,
    InlineImageGalleryBlock,
    InlinePodcastBlock,
    InlineTweetBlock,
    InlineVideoBlock,
)
from ..utils import get_youtube_thumbnail_url
from ..serializers import (
    AdSerializer,
    ArticlePageField,
    AuthorSerializer,
    CommentSerializer,
    VideoPageField,
)

PER_PAGE = 25


class ArticleIndexPage(RoutablePageMixin, Page, TranslatableMixin):
    max_count = 1
    subpage_types = ["neucms.ArticlePage", "neucms.VideoPage"]

    class Meta:
        verbose_name = "Article Index Page"
        verbose_name_plural = "Article Index Pages"

    content_panels = Page.content_panels + []

    def articles_shortlist(self):
        return ArticlePage.objects.live().order_by("-last_published_at")[:4]

    def videos_shortlist(self):
        return VideoPage.objects.live().order_by("-last_published_at")[:4]

    def feeditems_queryset(self):
        return PostPage.objects.live().order_by("-last_published_at")

    @route(r"^articles/$", name="all_articles")
    def get_all_articles(self, request, *args, **kwargs):
        all_articles = ArticlePage.objects.live().order_by("-last_published_at")

        if request.GET.get("tag", None):
            tag = request.GET.get("tag")
            all_articles = all_articles.filter(tags__slug__in=[tag])

        paginator = Paginator(all_articles, PER_PAGE)
        page = request.GET.get("page")

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return self.render(
            request,
            context_overrides={"articles": articles},
            template="neucms/article_index_page.html",
        )

    @route(r"^videos/$", name="all_videos")
    def get_all_videos(self, request, *args, **kwargs):
        all_videos = VideoPage.objects.live().order_by("-last_published_at")

        if request.GET.get("tag", None):
            tag = request.GET.get("tag")
            all_videos = all_videos.filter(tags__slug__in=[tag])

        paginator = Paginator(all_videos, PER_PAGE)
        page = request.GET.get("page")

        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)
        return self.render(
            request,
            context_overrides={"videos": videos},
            template="neucms/video_index_page.html",
        )

    @route(r"^(?P<category_slug>[\w-]+)/videos/(?P<page_slug>[\w-]+)")
    def get_video_page(self, request, page_slug, *args, **kwargs):
        page = get_object_or_404(VideoPage, slug=page_slug)
        context = {
            "page": page,
        }
        return render(request, "neucms/video_page.html", context)

    @route(r"^(?P<category_slug>[\w-]+)/(?P<page_slug>[\w-]+)")
    def get_article_page(self, request, page_slug, *args, **kwargs):
        page = get_object_or_404(ArticlePage, slug=page_slug)
        context = {
            "page": page,
        }
        return render(request, "neucms/article_page.html", context)


class HomePage(Page):
    subpage_types = [
        "neucms.CategoryPage",
        "neucms.FormPage",
        "neucms.ArticleIndexPage",
        "neucms.WebPage",
    ]

    intro = RichTextField(blank=True)
    page_snippets = ParentalManyToManyField(
        "neucms.PageSnippet", blank=True, related_name="home_pages"
    )
    show_popular_articles = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("show_popular_articles"),
        SnippetChooserPanel("page_snippets"),
        InlinePanel("page_sections", label="Page sections in this page"),
        InlinePanel("category_sections", label="Category sections in this page"),
    ]

    @property
    def popular_articles(self):
        today = date.today()
        start_time = today - timedelta(days=30)
        return (
            ArticlePage.objects.annotate(likes_count=Count("liked_users"))
            .filter(last_published_at__gt=start_time)
            .live()
            .order_by("-likes_count")[:10]
        )

    @property
    def latest_videos(self):
        return VideoPage.objects.live().order_by("-last_published_at")[:5]

    @property
    def latest_comments(self):
        return CustomComment.objects.all().order_by("-submit_date")[:3]

    api_fields = [
        APIField("intro"),
        APIField("page_snippets"),
        APIField("show_popular_articles"),
        APIField("popular_articles", serializer=ArticlePageField()),
        APIField("latest_videos", serializer=VideoPageField()),
    ]


class CategoryPage(RoutablePageMixin, Page):
    subpage_types = ["CategoryPage"]
    parent_page_types = [HomePage]

    category_page_ad = models.ForeignKey(
        "neucms.CategoryPageAd",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="ad_category",
        help_text=_("AD to be displayed on the category page and the related Article Pages."),
    )

    content_panels = Page.content_panels + [
        FieldPanel("category_page_ad"),
    ]

    def articles_shortlist(self):
        return ArticlePage.objects.filter(category=self).live().order_by("-last_published_at")[:4]

    @property
    def articles(self):
        return ArticlePage.objects.filter(category=self).live().order_by("-last_published_at")

    @property
    def category_ad(self):
        CategoryPageAdModel = apps.get_model("neucms", "CategoryPageAd")
        return (
            self.category_page_ad or CategoryPageAdModel.objects.filter(all_categories=True).first()
        )

    def feeditems_queryset(self):
        return PostPage.objects.filter(category=self).live().order_by("-last_published_at")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        articles_in_category = (
            ArticlePage.objects.filter(category=self).live().order_by("-last_published_at")
        )
        paginator = Paginator(articles_in_category, PER_PAGE)
        page = request.GET.get("page")

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles
        return context

    @route(r"^videos/$", name="videos_in_category")
    def get_videos(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        videos_in_category = (
            VideoPage.objects.filter(category=self).live().order_by("-last_published_at")
        )
        paginator = Paginator(videos_in_category, PER_PAGE)
        page = request.GET.get("page")

        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        context["videos"] = videos
        return self.render(
            request,
            context_overrides={
                "videos": videos,
            },
            template="neucms/category_page_videos.html",
        )

    def __str__(self):
        return self.title

    api_fields = [
        APIField("articles", serializer=ArticlePageField()),
        APIField("category_ad", serializer=AdSerializer()),
    ]


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "neucms.PostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class PostPage(SeoMixin, Page):
    subpage_types = []
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    seo_content_type = SeoType.ARTICLE
    seo_twitter_card = TwitterCard.LARGE

    promote_panels = SeoMixin.seo_panels

    @property
    def liked_users_count(self):
        return self.liked_users.count()

    def add_comment(self, user, comment, content_type, current_site):
        import pytz

        comment = CustomComment(
            user=user,
            user_name=user.display_name,
            user_email=user.email,
            comment=comment,
            submit_date=datetime.now(pytz.utc),
            content_type=content_type,
            object_pk=self.id,
            site_id=current_site.id,
            page=self,
        )

        comment.save()


class ArticlePage(PostPage):
    summary = RichTextField(
        _("summary"),
        help_text="The summary of the article, shown at the top of the article.",
        blank=True,
    )
    category = models.ForeignKey(
        "neucms.CategoryPage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category_articles",
    )
    image = models.ForeignKey(
        "wagtailimages.Image", blank=True, null=True, on_delete=models.SET_NULL
    )
    body = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=[
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "image",
                        "code",
                        "blockquote",
                    ]
                ),
            ),
            ("image", InlineImageBlock()),
            ("video", InlineVideoBlock()),
            ("ad", InArticleGoogleAdBlock()),
            ("carousal", InlineCarousalBlock()),
            ("image_gallery", InlineImageGalleryBlock()),
            ("tweet", InlineTweetBlock()),
            ("podcasts", InlinePodcastBlock()),
            ("html_embeds", HTMLEmbedBlock()),
        ]
    )
    author = models.ForeignKey(
        "neucms.Author", blank=True, null=True, on_delete=models.SET_NULL, related_name="articles"
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary", classname="full"),
        FieldPanel("category"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("author"),
    ]

    @property
    def category_ad(self):
        CategoryPageAdModel = apps.get_model("neucms", "CategoryPageAd")
        return (
            self.category.category_page_ad
            or CategoryPageAdModel.objects.filter(all_categories=True).first()
        )

    def get_url_parts(self, request=None, *args, **kwargs):
        url_parts = super().get_url_parts(request=request)
        if url_parts is None:
            return None
        else:
            site_id, root_url, page_path = url_parts
            category_slug = slugify(self.category.title)
            new_page_path = page_path.replace(self.slug, f"{category_slug}/{self.slug}")
            return (site_id, root_url, new_page_path)

    @cached_property
    def category_title(self):
        if self.category:
            return self.category.title
        else:
            return "Other"

    @cached_property
    def author_name(self):
        if self.author:
            return self.author.name
        else:
            return "Web Desk"

    @property
    def rel_url(self):
        from django.contrib.sites.models import Site

        site = Site.objects.get_current()
        return self.relative_url(current_site=site)

    def get_absolute_url(self):
        return self.get_url()

    @property
    def image_url(self):
        if self.image:
            return self.image.get_rendition("fill-480x360").url

    api_fields = [
        APIField("summary"),
        APIField("image"),
        APIField("category"),
        APIField("last_published_at"),
        APIField("body"),
        APIField("author", serializer=AuthorSerializer()),
        APIField("liked_users_count"),
        APIField("article_comments", serializer=CommentSerializer()),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
    ]


class VideoPage(PostPage):
    video_url = StreamField([("video", EmbedBlock(required=True))], min_num=1, max_num=1)
    thumbnail_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("Image for thumbnail. Either upload image or add url"),
    )
    thumbnail_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text=_(
            "Url of the thumbnail image. Will be generated automatically for youtube videos."
        ),
    )
    description = RichTextField(
        _("description"),
        help_text="The description of the video article.",
        blank=True,
    )

    category = models.ForeignKey(
        "neucms.CategoryPage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category_videos",
    )

    @cached_property
    def category_title(self):
        if self.category:
            return self.category.title
        else:
            return "Other"

    @cached_property
    def author_name(self):
        return "Web Desk"

    @property
    def summary(self):
        return self.description

    @property
    def category_ad(self):
        CategoryPageAdModel = apps.get_model("neucms", "CategoryPageAd")
        return (
            self.category.category_page_ad
            or CategoryPageAdModel.objects.filter(all_categories=True).first()
        )

    @property
    def uploaded_thumbnail_url(self):
        if self.thumbnail_image:
            return self.thumbnail_image.get_rendition("fill-480x360").url

    @property
    def image_url(self):
        return self.thumbnail_url or self.uploaded_thumbnail_url

    @property
    def rel_url(self):
        from django.contrib.sites.models import Site

        site = Site.objects.get_current()
        return self.relative_url(current_site=site)

    def get_absolute_url(self):
        return self.get_url()

    def save(self, *args, **kwargs):
        video_link = self.video_url[0].value.url
        if not self.thumbnail_url and "youtube" in video_link:
            self.thumbnail_url = get_youtube_thumbnail_url(video_link)
        super().save(*args, **kwargs)

    content_panels = Page.content_panels + [
        StreamFieldPanel("video_url"),
        FieldPanel("description", classname="full"),
        FieldPanel("category"),
        FieldPanel("tags"),
        MultiFieldPanel(
            [
                ImageChooserPanel("thumbnail_image"),
                FieldPanel("thumbnail_url"),
            ],
            heading="Video Thumbnail",
        ),
    ]

    def get_url_parts(self, request=None, *args, **kwargs):
        url_parts = super().get_url_parts(request=request)
        if url_parts is None:
            return None
        else:
            site_id, root_url, page_path = url_parts
            category_slug = slugify(self.category.title)
            new_page_path = page_path.replace(self.slug, f"{category_slug}/videos/{self.slug}")
            return (site_id, root_url, new_page_path)

    @property
    def liked_users_count(self):
        return self.liked_users.count()

    api_fields = [
        APIField("video_url"),
        APIField("description"),
        APIField("last_published_at"),
        APIField("thumbnail_image"),
        APIField("thumbnail_url"),
        APIField("liked_users_count"),
        APIField("url"),
        APIField("category"),
        APIField("category_ad", serializer=AdSerializer()),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("description"),
    ]


class CustomComment(XtdComment):
    page = ParentalKey("neucms.PostPage", on_delete=models.CASCADE, related_name="article_comments")

    def save(self, *args, **kwargs):
        self.page = PostPage.objects.get(pk=self.object_pk)
        super(CustomComment, self).save(*args, **kwargs)


# Forms -------------
class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(AbstractEmailForm):
    intro = models.TextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
    ]


# Template for other pages -----
class WebPage(Page):
    summary = RichTextField(_("summary"), blank=True)
    body = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=[
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "image",
                        "code",
                        "blockquote",
                    ]
                ),
            ),
            ("image", InlineImageBlock()),
            ("video", InlineVideoBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary", classname="full"),
        StreamFieldPanel("body"),
    ]

    def __str__(self):
        return self.title
