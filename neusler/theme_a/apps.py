from django.apps import AppConfig


class ThemeAConfig(AppConfig):
    """
    App that contains all theme template files for the frontend site
    This should contain only template files.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "neusler.theme_a"
    label = "neuthemea"
