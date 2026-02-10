# extractors/html_extractor.py
from __future__ import annotations
from bs4 import BeautifulSoup, NavigableString
import re


BLOCKLIST_TAGS = {
    "script", "style", "noscript", "svg", "canvas",
    "header", "footer", "nav", "aside", "form"
}


def clean_html(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "lxml")

    # Remove junk tags
    for tag in soup.find_all(BLOCKLIST_TAGS):
        tag.decompose()

    # Remove hidden elements
    for tag in soup.select('[aria-hidden="true"], [style*="display:none"]'):
        tag.decompose()

    return soup


def extract_main_text(html: str) -> str:
    soup = clean_html(html)

    # Prefer semantic containers
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", id=re.compile("content|main", re.I))
        or soup.body
    )

    if not main:
        return ""

    parts = []

    for el in main.descendants:
        if isinstance(el, NavigableString):
            text = el.strip()
            if text:
                parts.append(text)
        elif el.name in {"h1", "h2", "h3"}:
            heading = el.get_text(strip=True)
            if heading:
                parts.append(f"\n## {heading}\n")

    text = " ".join(parts)

    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


def extract_text_from_html(html: str) -> str:
    if not html or not html.strip():
        return ""
    return extract_main_text(html)
