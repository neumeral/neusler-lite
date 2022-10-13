from django.test import TestCase

from ..models import Menu, MenuItem
from .utils import create_category_page, create_home_page, get_root_page


class TestMenu(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)
        cls.category_page = create_category_page(cls.home_page)

    def test_menu_creation(self):
        menu = Menu.objects.create(title='Main')
        self.assertIsNotNone(menu)

    def test_menu_item_creation(self):
        menu = Menu.objects.create(title='Main')
        menu_item = MenuItem(menu=menu, title='Category 1', link_page=self.category_page)
        self.assertIsNotNone(menu_item)

    def test_menu_item_link(self):
        menu = Menu.objects.create(title='Main')
        menu_item = MenuItem(menu=menu, title='Category 1', link_page=self.category_page)
        self.assertEqual(menu_item.url(), self.category_page.url)
