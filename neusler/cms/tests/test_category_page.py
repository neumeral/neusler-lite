from django.test import TestCase

from ..models import CategoryPageAd
from .utils import create_article_page, create_articleindex_page, create_category_page, create_home_page, get_root_page


class TestCategoryPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)
        cls.article_index = create_articleindex_page(cls.home_page)

    def test_category_page_creation(self):
        phy_category = create_category_page(self.home_page, 'Test Category')
        self.assertIsNotNone(phy_category.pk)

    def test_category_page_articles_shortlist(self):
        category1 = create_category_page(self.home_page, 'Test')
        category2 = create_category_page(self.home_page, 'Hello')
        for i in range(10):
            create_article_page(self.article_index, title=f"Hello Test {i}", category=category1)

        create_article_page(self.article_index, title="Test 3")
        create_article_page(self.article_index, title="Test 4", category=category2)

        self.assertEqual(len(category1.articles_shortlist()), 4)
        category1_titles = map(lambda x: x.title, category1.articles_shortlist())
        self.assertTrue(all([title.startswith('Hello Test') for title in category1_titles]))

    def test_category_page_category_ad(self):
        ad = CategoryPageAd.objects.create(ad_title='Test Ad')
        CategoryPageAd.objects.create(ad_title='Test Ad All', all_categories=True)
        category_page = create_category_page(self.home_page, 'Test')
        category_page.category_page_ad = ad
        category_page.save()

        self.assertEqual(category_page.category_ad, ad)

    def test_category_page_category_ad_all_categories(self):
        ad = CategoryPageAd.objects.create(ad_title='Test Ad All', all_categories=True)
        category_page = create_category_page(self.home_page, 'Test')

        self.assertEqual(category_page.category_ad, ad)
