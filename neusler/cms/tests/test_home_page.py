from django.test import TestCase

from .utils import create_home_page, get_root_page


class TestHomePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()

    def test_root_page_exists(self):
        self.assertIsNotNone(self.root_page)
        self.assertTrue(self.root_page.is_root())

    def test_home_page_creation(self):
        home_page = create_home_page(self.root_page)

        self.assertIsNotNone(home_page.pk)
