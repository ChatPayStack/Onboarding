from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import hashlib
from pymongo import MongoClient
import os
from bson import ObjectId
from datetime import datetime, timezone


router = APIRouter()

client = MongoClient(os.getenv("MONGODB_URI"))


def _business_db_name(business_id: str) -> str:
    h = hashlib.sha1(business_id.encode()).hexdigest()[:8]
    return f"chatpay_b_{h}"


class OrdersRequest(BaseModel):
    business_id: str

class UpdateOrderStatusRequest(BaseModel):
    business_id: str
    order_id: str   

def serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    return obj

@router.post("/orders")
def get_all_orders(req: OrdersRequest):

    db_name = _business_db_name(req.business_id)
    db = client[db_name]

    orders_raw = list(
        db["orders"].find({}, {"_id": 0})
        .sort("created_at", -1)
    )

    orders = [serialize(o) for o in orders_raw]

    return {
        "business_id": req.business_id,
        "count": len(orders),
        "orders": orders
    }

@router.patch("/orders/status")
def update_order_status(req: UpdateOrderStatusRequest):

    db_name = _business_db_name(req.business_id)
    db = client[db_name]

    result = db["orders"].update_one(
        {"_id": ObjectId(req.order_id)},
        {
            "$set": {
                "status": "success",
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "message": "Order status updated to success",
        "order_id": req.order_id
    }