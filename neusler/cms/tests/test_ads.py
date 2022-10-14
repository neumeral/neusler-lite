from django.test import TestCase

from ..models import CategoryPageAd
from .utils import get_root_page


class TestAds(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = get_root_page()

    def test_categorypage_ad_model_creation(self):
        ad = CategoryPageAd.objects.create(ad_title="Test")
        self.assertIsNotNone(ad.pk)
