from django.urls import path

from .views import SearchAPI

urlpatterns = [
    path("", SearchAPI.as_view(), name="search"),
]
