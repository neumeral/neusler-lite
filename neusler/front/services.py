from .models import ArticleLike


def if_page_is_liked(page, user):
    if ArticleLike.objects.filter(user=user, article=page):
        return True
    return False


def get_page_likes(page):
    likes = ArticleLike.objects.filter(article=page).count()
    return likes


def like_unlike_page(page, user):
    if ArticleLike.objects.filter(user=user, article=page).exists():
        ArticleLike.objects.filter(user=user, article=page).delete()
        return False
    else:
        ArticleLike.objects.create(user=user, article=page)
        return True
