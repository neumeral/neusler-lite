from django.test import TestCase

from ..models import User


class TestUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="john", password="password", first_name="John", last_name="Doe"
        )

    def test_full_name_of_user(self):
        expected_fullname = "John Doe"
        self.assertEqual(expected_fullname, self.user.full_name)

    def test_short_name(self):
        expected_shortname = "John"
        self.assertEqual(expected_shortname, self.user.get_short_name())
