# extractors/product_extractor.py
from __future__ import annotations
from typing import List, Dict


def normalize_price(variant: Dict) -> float | None:
    price = variant.get("price")
    try:
        return float(price) if price is not None else None
    except Exception:
        return None


def extract_products_from_products_json(
    products_json: Dict,
    root_url: str,
) -> List[Dict]:
    products = []

    for p in products_json.get("products", []):
        variants = p.get("variants", [])

        price = None
        if variants:
            price = normalize_price(variants[0])

        products.append(
            {
                "external_id": p.get("id"),
                "handle": p.get("handle"),
                "name": p.get("title"),
                "description": p.get("body_html", ""),
                "price": price,
                "currency": p.get("currency"),
                "images": [img.get("src") for img in p.get("images", []) if img.get("src")],
                "url": f"{root_url.rstrip('/')}/products/{p.get('handle')}",
                "available": any(v.get("available") for v in variants),
                "raw": p,  # keep raw for debugging / enrichment
            }
        )

    return products


def attach_collections(
    products: List[Dict],
    collections_json: Dict,
) -> List[Dict]:
    collection_map = {}

    for c in collections_json.get("collections", []):
        collection_map[c.get("id")] = c.get("title")

    for p in products:
        # Shopify does not directly embed collection IDs in products.json
        # This is a placeholder for future enrichment
        p["collections"] = []

    return products
