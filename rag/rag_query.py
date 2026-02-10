# rag/rag_query.py
from openai import OpenAI
from db import get_db
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_rag(business_id: str, query: str, top_k: int = 5):
    db = get_db()

    # embed query
    emb = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        input=query,
    ).data[0].embedding

    # vector search (cosine via $vectorSearch or manual later)
    results = (
        db["vectors"]
        .find({"business_id": business_id})
        .limit(top_k)
    )

    context = "\n\n".join(r["text"] for r in results)

    # final answer
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer using the provided product context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
    )

    return resp.choices[0].message.content
