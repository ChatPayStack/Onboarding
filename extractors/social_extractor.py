import re
from urllib.parse import urlparse

SOCIAL_DOMAINS = {
    "instagram.com": "instagram",
    "facebook.com": "facebook",
    "tiktok.com": "tiktok",
    "twitter.com": "twitter",
    "x.com": "twitter",
    "linkedin.com": "linkedin",
    "youtube.com": "youtube",
}


def extract_social_links(html: str):
    links = set(re.findall(r'href=["\'](.*?)["\']', html))
    socials = {}

    for link in links:
        try:
            host = urlparse(link).netloc.lower()
        except Exception:
            continue

        for domain, name in SOCIAL_DOMAINS.items():
            if domain in host:
                socials[name] = link

    return socials