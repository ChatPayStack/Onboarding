import re
from urllib.parse import urljoin, urlparse
import httpx

KEYWORDS = [
    "policy", "privacy", "terms", "return", "refund",
    "shipping", "delivery", "about", "contact"
]

def discover_footer_links(root_url: str):
    html = httpx.get(root_url.rstrip("/")).text
    links = set(re.findall(r'href=["\'](.*?)["\']', html))

    urls = set()
    root_host = urlparse(root_url).netloc

    for link in links:
        full = urljoin(root_url, link)
        host = urlparse(full).netloc
        if host != root_host:
            continue
        if any(k in full.lower() for k in KEYWORDS):
            urls.add(full)

    return list(urls)