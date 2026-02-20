from celery import Celery
from app.core.config import settings
from app.db.session import init_db, SessionLocal
from app.db import models
from app.services.runner import run_pipeline_sync

celery_app = Celery("drawing_extractor", broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task(name="run_pipeline_task")
def run_pipeline_task(doc_id: str, pipeline_name: str):
    init_db()
    db = SessionLocal()
    try:
        doc = db.get(models.Document, doc_id)
        if not doc:
            return {"error": "Document not found"}
        try:
            result_path = run_pipeline_sync(doc_id, pipeline_name)
            doc.status = "done"
            doc.error = None
            db.merge(doc)
            db.merge(models.ExtractionResult(doc_id=doc_id, json_path=result_path))
            db.commit()
            return {"doc_id": doc_id, "status": "done"}
        except Exception as e:
            doc.status = "failed"
            doc.error = str(e)
            db.merge(doc)
            db.commit()
            return {"doc_id": doc_id, "status": "failed", "error": str(e)}
    finally:
        db.close()
