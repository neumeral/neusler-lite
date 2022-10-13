from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.core.models import Page
from wagtail.search.models import Query

from neusler.cms.models import ArticlePage, PostPage, VideoPage

from .serializers import ArticleResultsSerializer, VideoResultsSerializer


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    # Search
    if search_query:
        search_results = PostPage.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "neusearch/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )


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
        return Response([video_serializer.data, article_serializer.data])
