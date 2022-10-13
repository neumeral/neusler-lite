from django.urls import path

from neusler.cms.feed.views import BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed

urlpatterns = [
    # RSS feed
    path("basic/<slug:feed_slug>.rss", BasicFeed(), name="basic_feed"),
    path("extended/<slug:feed_slug>.rss", ExtendedFeed(), name="extended_feed"),
    # JSON feed
    path("basic/<slug:feed_slug>.json", BasicJsonFeed(), name="basic_json_feed"),
    path("extended/<slug:feed_slug>.json", ExtendedJsonFeed(), name="extended_json_feed"),
]
