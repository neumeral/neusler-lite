1. Run the following commands to reset the data

-   `make resetdb`
-   `make loadusers`

2. Delete media folder and recreate

-   `rm -rf media`
-   `mkdir -p media/images media/author_photos media/original_images media/user_avatars`

3. Run the server

-   `python manage.py runserver`

4. Upload images from sample/original_images from admin

-   Use url http://localhost:8000/admin/images/

5. Generate image renditions

-   `python manage.py generate_image_renditions`

6. Change image_ids in loader data

-   Make changes to `load_article_data.py` for image ids

7. Load sites and authors

-   `python manage.py loaddata sample/sites.json sample/authors.json`

8. Load article data

-   `python manage.py load_article_data`

9. Copy assets

-   `make copyassets`

10. Add video articles

-   https://www.youtube.com/watch?v=oI_X2cMHNe0 How Electricity Actually Works
-   https://www.youtube.com/watch?v=6etTERFUlUI The Absurd Search For Dark Matter

11. Update last published_at

-   `python manage.py update_published_at`

12. Add site data from admin

-   Add menu items
-   Add page snippets - Best of the week, Featured
-   Add home page ad and category ad
-   Update homepage to add snippets, categories etc

13. Map site to new home page

14. Run dumpdata (take a backup of the sample folder if required)

-   `make dumpdata`
