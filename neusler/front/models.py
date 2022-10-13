from django.db import models
from django.contrib.auth import get_user_model

from neusler.cms.models import PostPage

UserModel = get_user_model()


class ArticleLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="liked_articles")
    article = models.ForeignKey(PostPage, on_delete=models.CASCADE, related_name="liked_users")
