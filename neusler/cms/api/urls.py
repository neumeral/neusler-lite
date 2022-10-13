from django.urls import path

from .views import ArticleLikeAPI, FavouriteArticlesAPI, PostCommentAPI

urlpatterns = [
    path("favourite-articles/", FavouriteArticlesAPI.as_view(), name="favourite_articles"),
    path("like/<int:article_id>/", ArticleLikeAPI.as_view(), name="like_dislike_article"),
    path("comment/<article_id>/", PostCommentAPI.as_view(), name="post_comment"),
]
