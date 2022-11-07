from rest_framework import serializers

from neusler.cms.models import ArticlePage, VideoPage


class ArticleResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePage
        fields = [
            "id",
            "title",
            "summary",
            "category_title",
            "image_url",
            "url",
            "liked_users_count",
        ]


class VideoResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPage
        fields = [
            "id",
            "title",
            "video_url",
            "description",
            "thumbnail_image",
            "thumbnail_url",
        ]
