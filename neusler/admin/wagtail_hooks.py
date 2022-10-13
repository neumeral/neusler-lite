from django.urls import reverse

from wagtail import hooks
from wagtail.admin import widgets as wagtailadmin_widgets

from neusler.cms.models import ArticleIndexPage, ArticlePage, VideoPage


@hooks.register("register_icons")
def register_fa_icons(icons):
    icons.append("neusler/icons/ab-ads.svg")
    icons.append("neusler/icons/ab-bag-shopping-solid.svg")
    icons.append("neusler/icons/ab-bell-regular.svg")
    icons.append("neusler/icons/ab-bell-solid.svg")
    icons.append("neusler/icons/ab-book-open-solid.svg")
    icons.append("neusler/icons/ab-bookmark-regular.svg")
    icons.append("neusler/icons/ab-bookmark-solid.svg")
    icons.append("neusler/icons/ab-box-archive-solid.svg")
    icons.append("neusler/icons/ab-box-open-solid.svg")
    icons.append("neusler/icons/ab-bullhorn-solid.svg")
    icons.append("neusler/icons/ab-calendar-day-solid.svg")
    icons.append("neusler/icons/ab-chart-pie-solid.svg")
    icons.append("neusler/icons/ab-check-double-solid.svg")
    icons.append("neusler/icons/ab-clipboard-list-solid.svg")
    icons.append("neusler/icons/ab-clock-solid.svg")
    icons.append("neusler/icons/ab-coins-solid.svg")
    icons.append("neusler/icons/ab-comments-solid.svg")
    icons.append("neusler/icons/ab-cookie-solid.svg")
    icons.append("neusler/icons/ab-cubes-solid.svg")
    icons.append("neusler/icons/ab-database-solid.svg")
    icons.append("neusler/icons/ab-earth-asia-solid.svg")
    icons.append("neusler/icons/ab-envelope-open-text-solid.svg")
    icons.append("neusler/icons/ab-envelopes-bulk-solid.svg")
    icons.append("neusler/icons/ab-facebook.svg")
    icons.append("neusler/icons/ab-gauge-high-solid.svg")
    icons.append("neusler/icons/ab-google-plus-g.svg")
    icons.append("neusler/icons/ab-graduation-cap-solid.svg")
    icons.append("neusler/icons/ab-hand-holding-dollar-solid.svg")
    icons.append("neusler/icons/ab-heart-regular.svg")
    icons.append("neusler/icons/ab-heart-solid.svg")
    icons.append("neusler/icons/ab-house-chimney-solid.svg")
    icons.append("neusler/icons/ab-id-card-regular.svg")
    icons.append("neusler/icons/ab-indian-rupee-sign.svg")
    icons.append("neusler/icons/ab-key-solid.svg")
    icons.append("neusler/icons/ab-linkedin.svg")
    icons.append("neusler/icons/ab-location-dot-solid.svg")
    icons.append("neusler/icons/ab-location-pin-solid.svg")
    icons.append("neusler/icons/ab-mailchimp.svg")
    icons.append("neusler/icons/ab-message-solid.svg")
    icons.append("neusler/icons/ab-meta.svg")
    icons.append("neusler/icons/ab-money-bill-wave-solid.svg")
    icons.append("neusler/icons/ab-newspaper-solid.svg")
    icons.append("neusler/icons/ab-puzzle.svg")
    icons.append("neusler/icons/ab-reddit.svg")
    icons.append("neusler/icons/ab-shapes-solid.svg")
    icons.append("neusler/icons/ab-share-nodes.svg")
    icons.append("neusler/icons/ab-trash-can-regular.svg")
    icons.append("neusler/icons/ab-whatsapp.svg")
    icons.append("neusler/icons/ab-folder-tree-solid.svg")
    icons.append("neusler/icons/ab-file-circle-plus-solid.svg")
    icons.append("neusler/icons/ab-folder-open-solid.svg")
    icons.append("neusler/icons/ab-lightbulb-solid.svg")
    icons.append("neusler/icons/ab-twitter.svg")
    icons.append("neusler/icons/ab-shield-solid.svg")
    icons.append("neusler/icons/ab-shield-halved-solid.svg")
    icons.append("neusler/icons/ab-podcast.svg")

    # From other sources
    icons.append("neusler/icons/ax-google-analytics.svg")
    icons.append("neusler/icons/ax-google-adsense.svg")
    icons.append("neusler/icons/ax-firebase.svg")

    return icons


@hooks.register("register_page_listing_buttons")
def page_listing_buttons(page, page_perms, is_parent=False, next_url=None):
    if page.is_root():
        classes = {"button", "button-small", "button-secondary"}
        index_page = ArticleIndexPage.objects.first()
        if index_page:
            yield wagtailadmin_widgets.Button(
                "Add Article",
                reverse("wagtailadmin_pages:add_subpage", args=[index_page.id]),
                classes=classes,
                icon_name="ab-circle-plus-solid",
                priority=60,
            )


# FIXME: If index_page does not exist, this return None,
# which gets added to the admin_menu_items throwing an error

# @hooks.register("register_admin_menu_item")
# def register_add_article_item():
#     index_page = ArticleIndexPage.objects.first()
#     if index_page:
#         add_page_url = (reverse("wagtailadmin_pages:add_subpage", args=[index_page.id]),)
#         yield MenuItem(
#             "Add Article", add_page_url, icon_name="ab-file-circle-plus-solid", order=110
#         )


@hooks.register("register_page_listing_buttons")
def page_custom_listing_buttons(page, page_perms, is_parent=True, next_url=None):
    index_page = ArticleIndexPage.objects.first()
    if index_page and page.slug == index_page.slug:
        yield wagtailadmin_widgets.ButtonWithDropdownFromHook(
            "Filter",
            hook_name="page_filter_hook",
            page=page,
            page_perms=page_perms,
            is_parent=is_parent,
            next_url=next_url,
            priority=50,
        )


@hooks.register("page_filter_hook")
def page_custom_listing_more_buttons(page, page_perms, is_parent=False, next_url=None):
    yield wagtailadmin_widgets.Button("All", "?type=all", priority=10)
    yield wagtailadmin_widgets.Button("Articles", "?type=article", priority=20)
    yield wagtailadmin_widgets.Button("Videos", "?type=video", priority=30)


@hooks.register("construct_explorer_page_queryset")
def filter_based_on_page_type(parent_page, pages, request):
    index_page = ArticleIndexPage.objects.first()
    if index_page and parent_page.slug == index_page.slug:
        if request.GET.get("type", None) == "article":
            pages = pages.type(ArticlePage)
        elif request.GET.get("type", None) == "video":
            pages = pages.type(VideoPage)

    return pages
