import re
import httpx
from datetime import datetime, timezone

INFO_PATTERNS = [
    "/pages/",
    "/blogs/",
    "/policies/",
    "/about",
    "/faq",
    "/shipping",
    "/returns",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RAGBot/1.0)"}


def _now():
    return datetime.now(timezone.utc)


def extract_locs(xml: str):
    return re.findall(r"<loc>(.*?)</loc>", xml)


def is_info_url(url: str) -> bool:
    return any(p in url.lower() for p in INFO_PATTERNS)


def crawl_info_pages(root_url: str):
    pages = []

    with httpx.Client(timeout=20) as client:
        # 1️⃣ Load sitemap index
        index_url = root_url.rstrip("/") + "/sitemap_index.xml"
        index_resp = client.get(index_url, headers=HEADERS)
        sitemap_urls = extract_locs(index_resp.text)

        # 2️⃣ Load each child sitemap
        for sm_url in sitemap_urls:
            sm_resp = client.get(sm_url, headers=HEADERS)
            urls = extract_locs(sm_resp.text)

            for url in urls:
                if not is_info_url(url):
                    continue

                r = client.get(url, headers=HEADERS)
                if r.status_code != 200:
                    continue

                pages.append({
                    "url": url,
                    "html": r.text,
                    "page_type": "info",
                    "status_code": r.status_code,
                    "fetched_at": _now(),
                    "source": "shopify",
                })

    return pages
