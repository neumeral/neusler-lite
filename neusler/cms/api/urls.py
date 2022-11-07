from django.urls import path

from .views import ArticleLikeAPI, FavouriteArticlesAPI, PostCommentAPI

urlpatterns = [
    path("favourites/", FavouriteArticlesAPI.as_view(), name="my_favourites"),
    path("articles/<int:article_id>/likes", ArticleLikeAPI.as_view(), name="like_dislike_article"),
    path("articles/<int:article_id>/comments", PostCommentAPI.as_view(), name="post_comment"),
]
