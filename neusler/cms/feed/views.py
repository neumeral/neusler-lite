# ----------------------------
# Based on https://github.com/chrisdev/django-wagtail-feeds
# License: MIT License
# ----------------------------

import json
from collections import OrderedDict
from urllib.parse import urljoin

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed, SyndicationFeed, rfc3339_date
from django.utils.html import strip_tags

from bs4 import BeautifulSoup
from wagtail.models import Page, Site
from wagtail.rich_text import expand_db_html

from neusler.cms.models import RSSFeed


def get_slug(url):
    url_parts = list(filter(None, url.split("/")))
    return url_parts[-1]


class CustomFeedGenerator(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(CustomFeedGenerator, self).root_attributes()
        attrs["xmlns:content"] = "http://purl.org/rss/1.0/modules/content/"
        return attrs

    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.startElement("content:encoded", {})

        content = "<![CDATA["
        if item.get("image", None):
            content += '<img src="%s"><hr>' % (item["image"])
        if item.get("content", None):
            content += item["content"]
        content += "]]>"

        # Adding content in this way do not escape content so make it suitable
        # for Feedburner and other services. If we use
        # handler.characters(content) then it will escape content and will not
        # work perfectly with Feedburner and other services.
        handler._write(content)

        handler.endElement("content:encoded")


class JSONFeed(SyndicationFeed):
    content_type = "application/json; charset=utf-8"

    def write(self, outfile, encoding):
        data = OrderedDict()
        data["version"] = "https://jsonfeed.org/version/1"
        data.update(self.add_root_elements())

        if self.items:
            item_element = []

        for item in self.items:
            item_element += [
                self.add_item_elements(item),
            ]

        data["items"] = item_element

        outfile.write(json.dumps(data))

    def add_item_elements(self, item):
        item_elements = OrderedDict()

        item_elements["id"] = get_slug(item["link"])
        item_elements["url"] = item["link"]
        item_elements["title"] = item["title"]
        if item["description"] is not None:
            item_elements["summary"] = item["description"]

        content = ""
        if "image" in item:
            if item.get("image", None):
                content += '<img src="%s"><hr>' % (item["image"])
        if "content" in item:
            if item.get("content", None):
                content += item["content"]
                item_elements["content_html"] = content

        if item["pubdate"] is not None:
            item_elements["date_published"] = rfc3339_date(item["pubdate"])

        return item_elements

    def add_root_elements(self):
        root_elements = OrderedDict()

        root_elements["title"] = self.feed["title"]
        root_elements["description"] = self.feed["description"]
        root_elements["home_page_url"] = self.feed["link"]

        if self.feed["feed_url"] is not None:
            root_elements["feed_url"] = self.feed["feed_url"]

        if self.feed["author_name"] is not None:
            root_elements["author"] = {"name": self.feed["author_name"]}

        if self.feed["author_link"] is not None:
            if type(root_elements.get("author", None)) is dict:
                root_elements["author"]["url"] = self.feed["author_link"]

        if self.feed["author_email"] is not None:
            if type(root_elements.get("author", None)) is dict:
                root_elements["author"]["email"] = self.feed["author_email"]

        return root_elements


DEFAULT_ITEM_LIMIT = 20


class DefaultFeed(Feed):
    def get_object(self, request, feed_slug):
        feed = RSSFeed.objects.filter(slug=feed_slug).first()
        if feed:
            self.use_images = feed.use_images or False
        site = Site.find_for_request(request)
        self.site_url = site.root_url
        self.limit = feed.limit or DEFAULT_ITEM_LIMIT
        return feed

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.link

    def description(self, obj):
        return obj.description

    def author_name(self, obj):
        return obj.author_name

    def author_email(self, obj):
        return obj.author_email

    def author_link(self, obj):
        return obj.link

    def items(self, obj):
        page = obj.linked_page
        specific_page = page.get_specific()
        if page and hasattr(specific_page, "feeditems_queryset"):
            return specific_page.feeditems_queryset()[: self.limit]  # noqa
        else:
            return []

    def item_pubdate(self, item):
        return item.last_published_at

    def item_description(self, item):
        if issubclass(type(item), Page):
            return strip_tags(item.specific.summary)

    def item_link(self, item):
        if issubclass(type(item), Page):
            return item.specific.full_url
        else:
            return item.url

    def item_author_name(self, item):
        if issubclass(type(item), Page):
            return item.specific.author_name
        else:
            return None

    def item_author_email(self, item):
        if issubclass(type(item), Page):
            specific_page = item.get_specific()
            if hasattr(specific_page, "author"):
                if user := item.specific.author.user:
                    return user.email


class BasicFeed(DefaultFeed):
    # FEED TYPE
    feed_type = Rss201rev2Feed


class BasicJsonFeed(BasicFeed):
    # FEED TYPE
    feed_type = JSONFeed


class ExtendedFeed(DefaultFeed):
    # FEED TYPE
    feed_type = CustomFeedGenerator

    def item_content_field(self, item):
        if issubclass(type(item), Page):
            specific_page = item.get_specific()
            if hasattr(specific_page, "body"):
                return specific_page.body

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the 'add_item' call of the feed generator.
        Add the fields of the item, to be used by the custom feed generator.
        """
        fields_to_add = {}

        if self.use_images:
            if issubclass(type(item), Page):
                image_complete_url = urljoin(self.site_url, item.specific.image_url)
            else:
                image_complete_url = ""

        content_field = self.item_content_field(item)
        if content_field:
            try:
                content = expand_db_html(content_field)
            except Exception:
                content = content_field.__html__()

            soup = BeautifulSoup(content, "html.parser")
            # Remove style attribute to remove large bottom padding
            for div in soup.find_all("div", {"class": "responsive-object"}):
                del div["style"]
            # Add site url to image source
            for img_tag in soup.findAll("img"):
                if img_tag.has_attr("src"):
                    img_tag["src"] = urljoin(self.get_site_url(), img_tag["src"])

            fields_to_add["content"] = soup.prettify(formatter="html")

        if self.use_images:
            fields_to_add["image"] = image_complete_url
        else:
            fields_to_add["image"] = ""

        return fields_to_add


class ExtendedJsonFeed(ExtendedFeed):
    # FEED TYPE
    feed_type = JSONFeed
