from django.urls import path

from .views import SignupAPI, TokenAPI

urlpatterns = [
    path("api-token-auth/", TokenAPI.as_view(), name="api_token_auth"),
    path("signup/", SignupAPI.as_view(), name="signup_api"),
]
