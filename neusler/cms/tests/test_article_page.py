from django.test import TestCase

from .utils import create_article_page, create_articleindex_page, create_home_page, get_root_page


class TestArticlePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)
        cls.article_index = create_articleindex_page(cls.home_page)

    def test_article_page_creation(self):
        article_page = create_article_page(self.article_index)
        self.assertIsNotNone(article_page.pk)

    def test_article_page_category_title(self):
        pass

    def test_article_page_author_name(self):
        pass

    def test_article_page_relative_url(self):
        pass

    def test_article_page_like(self):
        pass

    def test_article_page_unlike(self):
        pass

    def test_article_page_liked_users_count(self):
        pass
