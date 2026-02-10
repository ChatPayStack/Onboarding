import httpx
from datetime import datetime, timezone
from extractors.html_extractor import extract_text_from_html
from chunker.text_chunker import build_chunk_docs
from db import get_db
from extractors.social_extractor import extract_social_links
from crawler.footer_links import discover_footer_links
def _now():
    return datetime.now(timezone.utc)


def process_info_pages(root_url: str, business_id: str, upload_batch_id: str):
    db = get_db()
    all_chunks = []
    processed_pages = []

    # ✅ already-ingested pages (file_id)
    existing_files = set(
        db["chunks"].distinct("file_id", {"business_id": business_id})
    )
    extra_urls = discover_footer_links(root_url)
    resp = httpx.get(f"{root_url.rstrip('/')}/pages.json?limit=250")
    data = resp.json()
    seen_files = set(existing_files)
    for p in data.get("pages", []):
        body_html = p.get("body_html")
        if not body_html:
            continue

        file_id = f"{root_url.rstrip('/')}/pages/{p.get('handle')}"
        processed_pages.append(file_id)
        if file_id in existing_files:
            continue  # ✅ skip duplicates
        if file_id in seen_files:
            continue
        seen_files.add(file_id)
        text = extract_text_from_html(body_html)
        if not text:
            continue

        chunks = build_chunk_docs(
            text=text,
            upload_batch_id=upload_batch_id,
            business_id=business_id,
            file_id=file_id,
            source_type="page",
        )

        all_chunks.extend(chunks)
    for url in extra_urls:
        processed_pages.append(url)
        page_resp = httpx.get(url)
        if url in seen_files:
            continue
        seen_files.add(url)
        if page_resp.status_code != 200:
            continue

        text = extract_text_from_html(page_resp.text)
        if not text:
            continue

        chunks = build_chunk_docs(
            text=text,
            upload_batch_id=upload_batch_id,
            business_id=business_id,
            file_id=url,
            source_type="page",
        )
        all_chunks.extend(chunks)
    if all_chunks:
        db["chunks"].insert_many(all_chunks)
    print("Processed pages:")
    for p in processed_pages:
        print("-", p)
    return {
        "pages": len(data.get("pages", [])),
        "chunks": len(all_chunks),
    }
