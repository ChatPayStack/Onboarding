# chunker/text_chunker.py
from __future__ import annotations
from typing import List, Dict
import hashlib


def _hash_text(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []

    chunks = []
    i = 0
    n = len(text)

    while i < n:
        j = min(n, i + max_chars)
        chunk = text[i:j].strip()
        if chunk:
            chunks.append(chunk)
        if j == n:
            break
        i = max(0, j - overlap)

    return chunks


def build_chunk_docs(
    *,
    text: str,
    upload_batch_id: str,
    business_id: str,
    file_id: str,
    source_type: str,
) -> List[Dict]:
    chunks = chunk_text(text)

    docs = []
    for idx, c in enumerate(chunks):
        docs.append(
            {
                "_id": f"{file_id}:{idx}:{_hash_text(c)[:10]}",
                "upload_batch_id": upload_batch_id,
                "business_id": business_id,
                "file_id": file_id,
                "source_type": source_type,
                "chunk_index": idx,
                "text": c,
            }
        )

    return docs
