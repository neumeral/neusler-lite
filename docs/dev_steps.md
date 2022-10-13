Create Database

```
DROP DATABASE neuslerdb;


CREATE USER wagu WITH PASSWORD 'password';
CREATE DATABASE neuslerdb OWNER wagu;
```


Change settings with dj_database_url, and python-decouple

Translations in django

Use i18n_patterns (from django.conf.urls.i18n import i18n_patterns) in urls
Add necessary configuration in settings.py, LANGUAGES, and localemiddleware

python manage.py makemessages -l fr -i venv # it throws error utf_8 unrecognized without venv
python manage.py compilemessages -l fr # create .mo file

## Learn

-   widget_tweaks

## Todo

-   Homepage

    -   Breaking News articles top article title scroll
    -   Highlighted articles section
    -   Latest News section

-   ArticlePage
    -   Breaking News section (with foreign key to )
    -   Best of the Week (with foreign key)
-   Sponsored
-   Category Page Ad
-   Videos
-   Recommended
-   Featured posts
-   Author

## - Featured Author

-   MenuItem
    -   Submenu
-   Newsletter
-   Subscription
