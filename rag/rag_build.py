# rag/rag_build.py
import os
from datetime import datetime, timezone
from typing import List, Dict, Any

from openai import OpenAI
from db import get_db

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _now():
    return datetime.now(timezone.utc)


def _embed_model():
    return os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


def _batched(lst: List[Any], n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def build_rag_index(business_id: str, upload_batch_id: str) -> Dict[str, Any]:
    db = get_db()

    # mark building
    db["rag_state"].update_one(
        {"_id": upload_batch_id},
        {
            "$set": {
                "_id": upload_batch_id,
                "business_id": business_id,
                "upload_batch_id": upload_batch_id,
                "status": "building",
                "updated_at": _now(),
            },
            "$setOnInsert": {"created_at": _now()},
        },
        upsert=True,
    )

    # ---- load chunks (sync pymongo) ----
    chunks = list(
        db["chunks"].find({"upload_batch_id": upload_batch_id})
    )

    # ---- load products (ONE DOC PER PRODUCT) ----
    products = list(
        db["products_final"].find({"upload_batch_id": upload_batch_id})
    )

    items: List[Dict[str, Any]] = []

    # ---- info chunks ----
    for c in chunks:
        t = (c.get("text") or "").strip()
        if not t:
            continue
        if not t or len(t) > 6000:   # safety guard
            continue

        items.append(
            {
                "kind": "chunk",
                "chunk_id": c["_id"],
                "file_id": c.get("file_id"),
                "source_type": c.get("source_type"),
                "chunk_index": c.get("chunk_index"),
                "title": f"{(c.get('source_type') or 'doc').upper()} • {c.get('file_id','')} • chunk {c.get('chunk_index',0)}",
                "text": t,
            }
        )

    # ---- product docs ----
    for i, p in enumerate(products):
        desc = (p.get("description") or "")[:4000]
        line = (
            f"PRODUCT: {p.get('name','')}\n"
            f"PRICE: {p.get('price')}\n"
            f"DESC: {desc}"
        )

        items.append(
            {
                "kind": "product",
                "chunk_id": f"product:{upload_batch_id}:{i}",
                "file_id": None,
                "source_type": "product",
                "chunk_index": i,
                "text": line,
                "name": p.get("name"),
                "price": p.get("price"),
                "description": p.get("description"),
                "asset_ids": p.get("images", []),
                "product_index": i,
            }
        )

    if not items:
        db["rag_state"].update_one(
            {"_id": upload_batch_id},
            {"$set": {"status": "empty", "updated_at": _now(), "count": 0}},
        )
        return {"upload_batch_id": upload_batch_id, "status": "empty", "count": 0}

    # ---- rebuild vectors idempotently ----
    db["vectors"].delete_many({"upload_batch_id": upload_batch_id})

    model = _embed_model()
    embedded = 0

    for batch in _batched(items, 64):
        texts = [x["text"] for x in batch]

        resp = client.embeddings.create(
            model=model,
            input=texts,
        )

        vec_docs = []
        for x, emb in zip(batch, resp.data):
            vec_docs.append(
                {
                    "_id": x["chunk_id"],
                    "business_id": business_id,
                    "upload_batch_id": upload_batch_id,
                    "kind": x["kind"],
                    "type": "product" if x["kind"] == "product" else "info",
                    "chunk_id": x["chunk_id"],
                    "file_id": x.get("file_id"),
                    "source_type": x.get("source_type"),
                    "chunk_index": x.get("chunk_index"),
                    "title": x.get("title"),
                    "name": x.get("name"),
                    "price": x.get("price"),
                    "description": x.get("description"),
                    "asset_ids": x.get("asset_ids", []),
                    "product_index": x.get("product_index"),
                    "text": x["text"],
                    "embedding": emb.embedding,
                    "model": model,
                    "created_at": _now(),
                }
            )

        if vec_docs:
            db["vectors"].insert_many(vec_docs)

        embedded += len(batch)

        db["rag_state"].update_one(
            {"_id": upload_batch_id},
            {"$set": {"embedded": embedded, "total": len(items), "updated_at": _now()}},
        )

    db["rag_state"].update_one(
        {"_id": upload_batch_id},
        {
            "$set": {
                "status": "ready",
                "updated_at": _now(),
                "count": embedded,
                "model": model,
            }
        },
    )

    return {
        "upload_batch_id": upload_batch_id,
        "status": "ready",
        "count": embedded,
        "model": model,
    }
