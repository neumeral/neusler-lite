from django.core.management.base import BaseCommand
from django.db import connection

TABLES = [
    "neucms_articlelike",
    "neucms_articlepagetag",
    "neucms_author",
    "neucms_categorypage",
    "neucms_articlepage",
    "neucms_customcomment",
    "neucms_homepage",
    "neucms_twocolumnarticleindexpage",
]


class Command(BaseCommand):
    help = "Truncates application data"
    """
    Assumes that the application user has CREATEDB permissions
    """

    def handle(self, *args, **options):
        db_name = connection.settings_dict["NAME"]

        self.stdout.write(self.style.NOTICE("Truncating tables ..."))
        truncate_sqls = []
        for table in TABLES:
            truncate_sqls.append(f"TRUNCATE TABLE {table} CASCADE;")

        sql = " ".join(truncate_sqls)

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS(f"Successfully truncated data in {db_name}."))
