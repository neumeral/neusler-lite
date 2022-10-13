from django.test import TestCase

from .utils import create_home_page, get_root_page
from ..models import ArticleIndexPage


class TestArticleIndexPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)

    def test_articleindex_page_creation(self):
        articleindex_page = ArticleIndexPage(title="All Articles", slug="all")
        self.home_page.add_child(instance=articleindex_page)
        articleindex_page.save()

        self.assertIsNot(articleindex_page.id, None)
        self.assertEquals(articleindex_page.get_parent(), self.home_page)
        self.assertEquals(articleindex_page.depth, 3)

    def test_articleindex_articles_shortlist(self):
        pass
