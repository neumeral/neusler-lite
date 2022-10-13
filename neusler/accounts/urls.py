from django.urls import path

from .views import (
    CustomPasswordChangeView,
    FavouriteArticlesView,
    MyCommentListView,
    UserProfileDisplayView,
    UserProfileView,
)

urlpatterns = [
    path("profile/edit/", UserProfileView.as_view(), name="account_profile_edit"),
    path("profile/", UserProfileDisplayView.as_view(), name="account_profile"),
    # To use default password change form of django-allauth
    # from allauth.account.views import password_change
    #
    # path("password/change/", password_change, name="settings_change_password"),
    #
    path(
        "password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path("me/favourites/", FavouriteArticlesView.as_view(), name="favourite_articles"),
    path("me/comments/", MyCommentListView.as_view(), name="my_comments"),
]
