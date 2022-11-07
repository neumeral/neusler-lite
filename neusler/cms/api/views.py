from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import ArticlePage, PostPage, VideoPage
from .serializers import FavouriteArticleSerializer


class FavouriteArticlesAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        favourites = ArticlePage.objects.filter(liked_users__user=user)
        serializer = FavouriteArticleSerializer(favourites, many=True)
        return Response(serializer.data)


class ArticleLikeAPI(APIView):
    def post(self, request, *args, **kwargs):
        article_id = kwargs.get("article_id")
        user = request.user
        try:
            article = PostPage.objects.get(id=article_id)
            if article:
                type = request.data.get("type")
                if type == "like":
                    article.like_article(user)
                elif type == "dislike":
                    article.unlike_article(user)
            return Response({"liked_users_count": article.liked_users_count})
        except PostPage.DoesNotExist:
            return Response({"message": "Invalid ID"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostCommentAPI(APIView):
    def post(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        article_id = kwargs.get("article_id")
        user = request.user
        comment = request.data.get("comment")
        try:
            if request.data.get("content_type") == "article":
                article = ArticlePage.objects.get(id=article_id)
                content_type = ContentType.objects.get_for_model(article)

                if article:
                    article.add_comment(user, comment, content_type, current_site)
            elif request.data.get("content_type") == "video":
                video = VideoPage.objects.get(id=article_id)
                content_type = ContentType.objects.get_for_model(video)
                if video:
                    video.add_comment(user, comment, content_type, current_site)
            else:
                return Response({"message": "Invalid content type"})
            return Response({"message": "Comment added"}, status=status.HTTP_201_CREATED)
        except PostPage.DoesNotExist:
            return Response({"message": "Invalid ID"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
