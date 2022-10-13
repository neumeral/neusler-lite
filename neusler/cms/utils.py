from urllib.parse import parse_qs, urlparse


def get_youtube_thumbnail_url(video_url):
    parsed_url = urlparse(video_url)
    video_id = parse_qs(parsed_url.query)["v"][0]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    return thumbnail_url
