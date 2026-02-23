from fastapi import FastAPI

from api.ingest import router as ingest_router
from api.query import router as query_router
from api.login import router as login_router
from api.orders import router as orders_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(login_router)
app.include_router(orders_router)