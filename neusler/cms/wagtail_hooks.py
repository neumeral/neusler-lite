from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

from wagtail.admin.menu import MenuItem, SubmenuMenuItem
from wagtail.contrib.modeladmin.menus import SubMenu
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks
from wagtail.snippets.models import register_snippet


from .models import CategoryPage, CategoryPageAd, RSSFeed

register_snippet(RSSFeed)
register_snippet(CategoryPageAd)


@hooks.register("construct_main_menu")
def hide_main_menu_items(request, menu_items):
    ignored_items = ("explorer", "snippets")
    menu_items[:] = [item for item in menu_items if item.name not in ignored_items]


@hooks.register("construct_settings_menu")
def hide_settings_menu_item(request, menu_items):
    ignored_items = (
        "google-tracking",
        "google-adsense",
    )
    menu_items[:] = [item for item in menu_items if item.name not in ignored_items]


@hooks.register("register_admin_menu_item")
def register_dashboard_menu_item():
    return MenuItem(
        "Dashboard", reverse("wagtailadmin_home"), icon_name="ab-shapes-solid", order=000
    )


@hooks.register("register_admin_menu_item")
def register_pages_menu_item():
    return MenuItem(
        "Pages", reverse("wagtailadmin_explore_root"), icon_name="ab-folder-open-solid", order=100
    )


class CategoriesAdmin(ModelAdmin):
    model = CategoryPage
    menu_label = "Categories"
    menu_icon = "ab-folder-tree-solid"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "title",
        "latest_revision_created_at",
        "live",
    )
    search_fields = ("title",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # only show category pages
        return qs.type(CategoryPage)


modeladmin_register(CategoriesAdmin)


@hooks.register("register_admin_menu_item")
def register_snippets_menu_item():
    return MenuItem(
        "Content Types", reverse("wagtailsnippets:index"), icon_name="ab-cubes-solid", order=300
    )


@hooks.register("register_admin_menu_item")
def register_integration_menu_item():
    tracking_settings_url = reverse(
        "wagtailsettings:edit",
        kwargs={"app_name": "neuadmin", "model_name": "AnalyticsSettings"},
    )
    googleads_settings_url = reverse(
        "wagtailsettings:edit",
        kwargs={"app_name": "neuads", "model_name": "GoogleAdsSetting"},
    )
    menu_items = [
        MenuItem("Google Tracking", tracking_settings_url, icon_name="ax-google-analytics"),
        MenuItem("Google Adsense", googleads_settings_url, icon_name="ax-google-adsense"),
    ]

    return SubmenuMenuItem("Integrations", SubMenu(menu_items), icon_name="ab-puzzle")


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    return format_html('<link rel="stylesheet" href="{}">', static("admin/css/styles.css"))


@hooks.register("insert_editor_css", order=100)
def admin_editor_css():
    """Add /static/css/custom.css to the admin."""
    return format_html('<link rel="stylesheet" href="{}">', static("admin/css/editor.css"))


# class UserbarDocumentationLinkItem:
#     def render(self, request):
#         return (
#             '<li class="wagtail-userbar__item" role="presentation"><a href="#" '
#             + 'target="_parent" role="menuitem" class="action icon icon-wagtail">Documentation</a></li>'
#         )


# @hooks.register("construct_wagtail_userbar")
# def add_userbar_link(request, items):
#     return items.append(UserbarDocumentationLinkItem())
