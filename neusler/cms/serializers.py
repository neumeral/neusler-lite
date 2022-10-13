from datetime import datetime, timedelta

import humanize
import pytz
from rest_framework.fields import Field
from wagtail.rich_text import get_text_for_indexing


class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class AdSerializer(Field):
    def to_representation(self, value):
        return {
            "title": value.ad_title,
            "image_url": value.ad_image.file.url,
            "image_title": value.ad_image.title,
            "image_width": value.ad_image.width,
            "image_height": value.ad_image.height,
            "url": value.ad_url,
        }


class ArticlePageField(Field):
    def to_representation(self, pages):
        return_values = []
        for page in pages:
            page_tags = list(map(lambda x: x.name, page.specific.tags.all()))
            page_summary = get_text_for_indexing(page.specific.summary)

            if page.specific.image:
                page_image = page.specific.image.file.url
            else:
                page_image = None

            article = {
                "id": page.id,
                "title": page.title,
                "image": page_image,
                "category": page.specific.category.title,
                "summary": page_summary,
                "last_published_at": page.last_published_at,
                "tags": page_tags,
                "url": page.url,
            }
            return_values.append(article)

        return return_values


class VideoPageField(Field):
    def to_representation(self, pages):
        return_values = []
        for page in pages:
            page_tags = list(map(lambda x: x.name, page.specific.tags.all()))
            page_description = get_text_for_indexing(page.specific.description)

            if page.specific.thumbnail_image:
                page_image = page.specific.image.file.url
            else:
                page_image = page.specific.thumbnail_url

            video = {
                "id": page.id,
                "title": page.title,
                "thumbnail": page_image,
                "category": page.specific.category.title,
                "description": page_description,
                "last_published_at": page.last_published_at,
                "tags": page_tags,
                "url": page.url,
            }
            return_values.append(video)

        return return_values


class BaseSnippetSerializer(Field):
    def to_representation(self, snippet):
        snippet_articles = []
        for page in snippet.section_articles:
            page_summary = get_text_for_indexing(page.specific.summary)
            if page.specific.image:
                page_image = page.specific.image.file.url
            else:
                page_image = None

            article = {
                "id": page.id,
                "title": page.title,
                "image": page_image,
                "category": page.specific.category.title,
                "summary": page_summary,
                "url": page.url,
            }
            snippet_articles.append(article)

        return {
            "title": snippet.title,
            "section_articles": snippet_articles,
        }


class AuthorSerializer(Field):
    def to_representation(self, author):
        return {
            "name": author.name,
            "designation": author.designation,
            "short_bio": author.short_bio,
            "photo": author.photo.url,
        }


class CommentSerializer(Field):
    def to_representation(self, article_comments):
        comments = []
        for comment in article_comments.all():
            time = comment.submit_date
            now = datetime.now(pytz.utc)
            if (now - time) < timedelta(days=2):
                time = humanize.naturaltime(now - time)
            comment_data = {
                "comment": comment.comment,
                "user": comment.name,
                "user_photo": comment.user.avatar.url,
                "time": time,
            }
        comments.append(comment_data)
        return {
            "comments": comments,
        }
