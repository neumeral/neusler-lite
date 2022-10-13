from rest_framework import serializers

from ..models import ArticlePage


class FavouriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePage
        fields = [
            "id",
            "title",
            "summary",
            "last_published_at",
            "category_title",
            "url",
            "image_url",
        ]
