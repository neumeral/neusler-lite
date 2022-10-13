from django.test import RequestFactory, TestCase

from ..models import User
from ..views import UserProfileView


class TestCustomUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create(username="john", password="password", first_name="John", last_name="Doe")

    def test_profile_view_with_user_gets_valid_response(self):
        request = self.factory.get(self.user.get_absolute_url())
        # log user in
        request.user = self.user
        self.assertEqual(UserProfileView.as_view()(request).status_code, 200)
