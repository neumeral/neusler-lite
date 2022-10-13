Run the following commands to reset the data

-   `make resetdb`

-   `make loadusers`

-   Delete media folder and recreate

    -   `rm -rf media`
    -   `mkdir -p media/images media/author_photos media/original_images media/user_avatars`

-   Run the server `python manage.py runserver`

-   Upload images from sample/original_images through http://localhost:8000/admin/images/

-   Generate image renditions `python manage.py generate_image_renditions`

-   Make changes to `load_article_data.py` for image ids

-   load sites and authors `python manage.py loaddata sample/sites.json sample/authors.json`

-   load article data - `python manage.py load_article_data`
-   copy assets - `make copyassets`
-   Add video articles

    -   https://www.youtube.com/watch?v=oI_X2cMHNe0 How Electricity Actually Works
    -   https://www.youtube.com/watch?v=6etTERFUlUI The Absurd Search For Dark Matter

-   Update last published_at `python manage.py update_published_at`

-   Add menu items
-   Add page snippets - Best of the week, Featured
-   Add home page ad and category ad

-   Update homepage to add snippets, categories etc

-   Map site to new home page
