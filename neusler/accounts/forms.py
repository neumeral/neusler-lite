from django import forms
from django.forms import ModelForm

from wagtail.users.forms import UserCreationForm, UserEditForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class CustomUserEditForm(UserEditForm):
    class Meta(UserEditForm.Meta):
        model = User
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "display_name", "date_of_birth", "city", "country", "avatar"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}
