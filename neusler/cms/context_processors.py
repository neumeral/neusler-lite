from wagtail.models import Site

from neusler.admin.models import GeneralSettings

from .models import ArticleIndexPage, FormPage, FooterSection


def sidebar(request):
    article_index = ArticleIndexPage.objects.first()
    recent_articles = recent_videos = []

    if article_index:
        recent_articles = article_index.articles_shortlist()
        recent_videos = article_index.videos_shortlist()

    newsletter = FormPage.objects.first()
    newsletter_form = None
    if newsletter:
        newsletter_form = newsletter.get_form(page=newsletter, user=request.user)
    return {
        "recent_articles": recent_articles,
        "recent_videos": recent_videos,
        "newsletter": newsletter,
        "newsletter_form": newsletter_form,
    }


def footer(request):
    footer_sections = FooterSection.objects.all()
    site = Site.find_for_request(request)
    site_details = GeneralSettings.for_site(site)
    return {
        "footer_sections": footer_sections,
        "site_details": site_details,
    }
