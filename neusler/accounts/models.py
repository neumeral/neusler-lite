from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class User(AbstractUser):
    display_name = models.CharField(_("display name"), max_length=50, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    city = models.CharField(_("city"), max_length=100, default="", blank=True)
    country = CountryField(_("country"), blank=True, null=True)
    avatar = models.ImageField(
        _("avatar"), upload_to="user_avatars/", default="user_avatars/default_avatar.png"
    )

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_absolute_url(self):
        return reverse("account_profile")

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def country_code(self):
        return str(self.country)
