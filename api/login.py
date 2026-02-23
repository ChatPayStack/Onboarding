from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_db
import uuid

router = APIRouter()


class LoginRequest(BaseModel):
    user_id: str
    password: str


@router.post("/login")
def login(req: LoginRequest):
    db = get_db()

    user = db["login"].find_one({
        "user_id": req.user_id,
        "password": req.password,  # TEMP: plain text
    })

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    updates = {}
    
    if not user.get("business_id"):
        updates["business_id"] = str(uuid.uuid4())

    if "upload_batch_id" not in user:
        updates["upload_batch_id"] = None

    if "telegram_bot_token" not in user:
        updates["telegram_bot_token"] = None

    if updates:
        db["login"].update_one(
            {"_id": user["_id"]},
            {"$set": updates},
        )
        user.update(updates)

    return {
        "user_id": user["user_id"],
        "business_id": user["business_id"],
        "upload_batch_id": user.get("upload_batch_id"),
    }
