from datetime import date, datetime, timedelta

from django import template
from django.db.models import Count

import humanize
import pytz

from wagtail.images import get_image_model
from wagtail.models import Collection

from neusler.cms.models import ArticlePage, Menu, PageSnippet

register = template.Library()


@register.simple_tag()
def get_snippet(slug):
    try:
        # see if there is a custom menu defined for the slug of the item
        candidates = PageSnippet.objects.get(slug=slug).snippet_articles.all()

        # create a list of all items that should be shown in the menu depending on logged_in
        snippet_articles = []
        for candidate in candidates:
            snippet_articles.append({"page": candidate.link_page, "url": candidate.url()})
        return snippet_articles
    except PageSnippet.DoesNotExist:
        return None


@register.simple_tag()
def get_first(array):
    if len(array) > 0:
        return array[0]


@register.simple_tag()
def except_first(array):
    if len(array) > 1:
        return array[1:]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag()
def get_menu(slug, logged_in):
    try:
        candidates = Menu.objects.get(slug=slug).menu_items.all()
        menu_items = []
        for candidate in candidates:
            if candidate.show(logged_in):

                menu_items.append(
                    {
                        "title": candidate.title,
                        "url": candidate.url(),
                        "slug": candidate.slug_of_submenu,
                        "icon": candidate.icon,
                    }
                )
        return menu_items
    except Menu.DoesNotExist:
        pass


@register.simple_tag()
def get_tag_link(tag, page_type="articles"):
    from neusler.cms.models import ArticleIndexPage

    article_index = ArticleIndexPage.objects.first()
    if article_index:
        return f"{article_index.url}{page_type}/?tag={tag}"
    else:
        return "#"


@register.simple_tag()
def get_news_blurb(slug):
    try:
        # see if there is a custom menu defined for the slug of the item
        posts = PageSnippet.objects.get(slug=slug).snippet_articles.all()[:6]

        # create a list of all items that should be shown in the menu depending on logged_in
        news_blurb_articles = []
        for post in posts:
            news_blurb_articles.append({"page": post.link_page, "url": post.url()})

        return news_blurb_articles
    except PageSnippet.DoesNotExist:
        return None


@register.simple_tag()
def get_news_blurb_trending():
    today = date.today()
    start_time = today - timedelta(days=30)
    return (
        ArticlePage.objects.annotate(likes_count=Count("liked_users"))
        .filter(last_published_at__gt=start_time)
        .live()
        .order_by("-likes_count")[:5]
    )


@register.simple_tag()
def humanize_time(time):
    now = datetime.now(pytz.utc)
    if (now - time) < timedelta(days=2):
        return humanize.naturaltime(now - time)
    return time


@register.simple_tag(takes_context=True)
def set_breakpoint(context, *args):
    """
    Set breakpoints in the template for easy examination of the context,
    or any variables of your choice.

    Usage:
        {% load breakpoint %}
        {% set_breakpoint %}
              - or -
        {% set_breakpoint your_variable your_other_variable %}

        When inside the breakpoint, get variables in context as follows:
        # context.get('page')

    - The context is always accessible in the pdb console as a dict 'context'.

    - Additional variables can be accessed as vars[i] in the pdb console.
      - e.g. in the example above, your_variable will called vars[0] in the
             console, your_other_variable is vars[1]
    """

    vars = [arg for arg in locals()["args"]]  # noqa F841
    breakpoint()


@register.simple_tag()
def get_collection_images(collection_id):
    collection = Collection.objects.get(pk=collection_id)
    ImageModel = get_image_model()
    images = ImageModel.objects.filter(collection=collection)
    return images
