from django.test import TestCase

from .utils import create_category_page, create_home_page, get_root_page


class TestVideoPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)
        cls.category_page = create_category_page(cls.home_page)

    def test_video_page_creation(self):
        pass
