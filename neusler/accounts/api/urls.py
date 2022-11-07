from django.urls import path

from .views import SignupAPI, TokenAPI

urlpatterns = [
    path("token/", TokenAPI.as_view(), name="token_api"),
    path("signup/", SignupAPI.as_view(), name="signup_api"),
]
