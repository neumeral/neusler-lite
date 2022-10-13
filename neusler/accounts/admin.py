from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from allauth.socialaccount.models import EmailAddress, SocialAccount, SocialApp, SocialToken


site_name = "Neusler"

admin.site.site_header = f"{site_name} Admin"
admin.site.site_title = f"{site_name} Admin Portal"
admin.site.index_title = f"{site_name}"


# admin.site.unregister(SocialAccount)
# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialToken)
# admin.site.unregister(EmailAddress)


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_filter = ["is_staff"]
    search_fields = ("username__startswith",)
    list_display = (
        "pk",
        "email",
        "username",
        "full_name",
        "is_superuser",
        "is_staff",
        "last_login",
    )
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Other info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "display_name",
                    "date_of_birth",
                    "city",
                    "country",
                    "avatar",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ]
            },
        ),
    ]

    def full_name(self, obj):
        return obj.get_full_name()
