from django.http import JsonResponse
from django.views import View

from neusler.cms.models import PostPage

from .services import get_page_likes, if_page_is_liked, like_unlike_page


class PageLikeView(View):
    def get(self, request, *args, **kwargs):
        return_values = {}
        page = request.GET.get("page")
        user = request.user
        if user.is_authenticated:
            page_is_liked = if_page_is_liked(page, user)
            return_values["page_is_liked"] = page_is_liked
        page_likes = get_page_likes(page)
        return_values["page_likes"] = page_likes
        return JsonResponse(return_values)

    def post(self, request, *args, **kwargs):
        page_id = request.POST.get("page_id")
        page = PostPage.objects.filter(pk=page_id).first()
        user = request.user
        return_values = {}
        page_liked = like_unlike_page(page, user)
        return_values["page_is_liked"] = page_liked
        return_values["page_likes"] = get_page_likes(page)
        return JsonResponse(return_values)
