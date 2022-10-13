from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from neusler.search import views as search_views
from neusler.search.views import SearchAPI

from .api import api_router

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("comments/", include("django_comments_xtd.urls")),
    path("cms/api/", include("neusler.cms.api.urls")),
    path("accounts/api/", include("neusler.accounts.api.urls")),
    path("rss/", include("neusler.cms.feed.urls")),
    path("front/", include("neusler.front.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    path("api/search/", SearchAPI.as_view(), name="search_api"),
    path("accounts/", include("neusler.accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/v2/", api_router.urls),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)
