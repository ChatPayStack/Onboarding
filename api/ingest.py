from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import httpx

from extractors.product_extractor import extract_products_from_products_json
from rag.rag_build import build_rag_index
from db import get_db
from pipelines.process_info_pages import process_info_pages

router = APIRouter()


class IngestRequest(BaseModel):
    url: str
    business_id: str


@router.post("/ingest")
def ingest(req: IngestRequest):
    upload_batch_id = str(uuid.uuid4())
    db = get_db()

    # 1️⃣ fetch products.json
    data = httpx.get(f"{req.url.rstrip('/')}/products.json?limit=250").json()
    products = extract_products_from_products_json(data, req.url)

    # 2️⃣ store products_final
    final_docs = []
    for p in products:
        final_docs.append({
            "upload_batch_id": upload_batch_id,
            "business_id": req.business_id,
            "external_id": p["external_id"],
            "handle": p["handle"],
            "name": p["name"],
            "description": p["description"],
            "price": p["price"],
            "currency": p["currency"],
            "images": p["images"],
            "url": p["url"],
            "available": p["available"],
        })

    if final_docs:
        db["products_final"].insert_many(final_docs)

    process_info_pages(
        root_url=req.url,
        business_id=req.business_id,
        upload_batch_id=upload_batch_id,
    )

    # 3️⃣ build RAG (sync, proven)
    build_rag_index(
        business_id=req.business_id,
        upload_batch_id=upload_batch_id,
    )
    db["login"].update_one(
        {"business_id": req.business_id},
        {"$set": {"upload_batch_id": upload_batch_id}},
    )
    return {
        "upload_batch_id": upload_batch_id,
        "products": len(final_docs),
        "status": "ready",
    }
