from fastapi import APIRouter
from app.api.routes_documents import router as documents_router

router = APIRouter()
router.include_router(documents_router, tags=["documents"])
