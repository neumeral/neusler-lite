from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.core.models import Page
from wagtail.search.models import Query

from neusler.cms.models import ArticlePage, VideoPage

from .serializers import ArticleResultsSerializer, VideoResultsSerializer


class SearchAPI(APIView):
    def get(self, request, *args, **kwargs):
        search_query = request.data.get("query", None)

        if search_query:
            article_results = ArticlePage.objects.live().search(search_query)
            video_results = VideoPage.objects.live().search(search_query)

            query = Query.get(search_query)

            # Record hit
            query.add_hit()
        else:
            article_results = Page.objects.none()
            video_results = Page.objects.none()

        article_serializer = ArticleResultsSerializer(article_results, many=True)
        video_serializer = VideoResultsSerializer(video_results, many=True)

        all_results = video_serializer.data + article_serializer.data
        return Response(all_results)
