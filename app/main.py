from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.logging import setup_logging
from app.db.session import init_db

setup_logging()

app = FastAPI(title="Engineering Drawing PDF Extractor", version="1.0.0")

@app.on_event("startup")
def _startup():
    init_db()

app.include_router(api_router, prefix="/api/v1")
