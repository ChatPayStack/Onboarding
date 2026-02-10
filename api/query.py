from fastapi import APIRouter
from pydantic import BaseModel
from rag.rag_query import query_rag

router = APIRouter()


class QueryRequest(BaseModel):
    business_id: str
    query: str


@router.post("/query")
def query(req: QueryRequest):
    answer = query_rag(
        business_id=req.business_id,
        query=req.query,
    )
    return {"answer": answer}
