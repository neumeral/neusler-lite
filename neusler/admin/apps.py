from django.apps import AppConfig


class NeuslerAdminConfig(AppConfig):
    """
    This is the app that contains all the admin changes for the base version of app.
    Other django apps in the project will extend the admin interface
    with wagtail hooks and more

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "neusler.admin"
    label = "neuadmin"

    def ready(self):
        import neusler.admin.signals  # noqa
