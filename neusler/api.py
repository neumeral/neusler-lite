from django.urls import include, path

from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

wagtail_api_router = WagtailAPIRouter("wagtailapi")

wagtail_api_router.register_endpoint("pages", PagesAPIViewSet)
wagtail_api_router.register_endpoint("images", ImagesAPIViewSet)
wagtail_api_router.register_endpoint("documents", DocumentsAPIViewSet)

urlpatterns = [
    path("accounts/", include("neusler.accounts.api.urls")),
    path("cms/", include("neusler.cms.api.urls")),
    path("comments/", include("django_comments_xtd.api.urls")),
    path("search/", include("neusler.search.api.urls")),
    path("", wagtail_api_router.urls),
]
