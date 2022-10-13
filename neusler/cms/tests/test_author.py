from django.test import TestCase

from ..models import Author


class TestAuthor(TestCase):
    def test_author_model_creation(self):
        author = Author.objects.create(name='John Doe')
        self.assertIsNotNone(author.pk)
