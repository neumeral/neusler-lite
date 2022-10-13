from django.urls import path

from .views import PageLikeView

urlpatterns = [
    path("article/like", PageLikeView.as_view(), name="like_unlike_page"),
]
