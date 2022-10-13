from django.contrib.sites.models import Site

from wagtail.models import Page

from ..models import ArticleIndexPage, ArticlePage, CategoryPage, HomePage


def get_root_page():
    return Page.objects.filter(depth=1).first()


def create_home_page(root_page):
    home_page = HomePage(title="Home Page")
    root_page.add_child(instance=home_page)
    home_page.save()
    site = Site.objects.get(id=1)
    site.root_page = home_page
    site.save()
    return home_page


def create_articleindex_page(home_page):
    articleindex_page = ArticleIndexPage(title='All Articles', slug='all')
    home_page.add_child(instance=articleindex_page)
    articleindex_page.save()
    return articleindex_page


def create_category_page(home_page, category_name='test'):
    category_page = CategoryPage(title=category_name)
    home_page.add_child(instance=category_page)
    category_page.save()
    return category_page


def get_category_page(category_name):
    category_page = CategoryPage.objects.filter(title=category_name).first()
    return category_page


def create_article_page(article_index_page, title='Test', category=None):
    category_page = None
    if category:
        category_page = get_category_page(category)

    article_page = ArticlePage(
        title=title,
        summary='test',
        body='[{"type": "paragraph", "value": "test"}]',
        category=category_page
    )
    article_index_page.add_child(instance=article_page)
    article_page.save()
    return article_page
