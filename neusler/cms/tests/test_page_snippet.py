from django.test import TestCase

from ..models import PageSnippet
from .utils import create_home_page, get_root_page


class TestPageSnippet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()
        cls.home_page = create_home_page(cls.root_page)

    def test_page_snippet_creation(self):
        ps = PageSnippet(title='Best of the week')
        ps.save()

        self.assertGreater(ps.pk, 0)

    def test_page_snippet_slug(self):
        ps = PageSnippet(title='Best of the week')
        ps.save()

        self.assertEqual(ps.slug, 'best-of-the-week')
