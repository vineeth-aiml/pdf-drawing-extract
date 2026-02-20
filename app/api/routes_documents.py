import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.db import models
from app.services.runner import run_pipeline_sync
from app.worker import run_pipeline_task

router = APIRouter()

def _doc_dir(doc_id: str) -> str:
    return os.path.join(settings.storage_dir, doc_id)

@router.post("/documents")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(settings.storage_dir, exist_ok=True)

    doc_id = str(uuid.uuid4())
    ddir = _doc_dir(doc_id)
    os.makedirs(ddir, exist_ok=True)

    pdf_path = os.path.join(ddir, "input.pdf")
    with open(pdf_path, "wb") as f:
        f.write(file.file.read())

    db.add(models.Document(id=doc_id, filename=file.filename, status="uploaded"))
    db.commit()

    return {"doc_id": doc_id, "filename": file.filename}

@router.post("/documents/{doc_id}/run")
def run_document(doc_id: str, pipeline: str = Query(default=None), db: Session = Depends(get_db)):
    doc = db.get(models.Document, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")

    chosen = pipeline or settings.pipeline_default
    doc.pipeline = chosen
    doc.status = "processing"
    doc.error = None
    db.commit()

    try:
        result_path = run_pipeline_sync(doc_id=doc_id, pipeline_name=chosen)

        doc.status = "done"
        db.merge(doc)
        db.merge(models.ExtractionResult(doc_id=doc_id, json_path=result_path))
        db.commit()

        return {"doc_id": doc_id, "status": "done", "pipeline": chosen}
    except Exception as e:
        # mark failed
        doc = db.get(models.Document, doc_id)
        if doc:
            doc.status = "failed"
            doc.error = str(e)
            db.merge(doc)
            db.commit()
        raise

@router.post("/documents/{doc_id}/run_async")
def run_document_async(doc_id: str, pipeline: str = Query(default=None), db: Session = Depends(get_db)):
    doc = db.get(models.Document, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")

    chosen = pipeline or settings.pipeline_default
    doc.pipeline = chosen
    doc.status = "processing"
    doc.error = None
    db.commit()

    run_pipeline_task.delay(doc_id, chosen)
    return {"doc_id": doc_id, "status": "queued", "pipeline": chosen}

@router.get("/documents/{doc_id}")
def get_status(doc_id: str, db: Session = Depends(get_db)):
    doc = db.get(models.Document, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return {
        "doc_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "pipeline": doc.pipeline,
        "error": doc.error,
    }

@router.get("/documents/{doc_id}/result")
def get_result(doc_id: str, db: Session = Depends(get_db)):
    r = db.get(models.ExtractionResult, doc_id)
    if not r:
        raise HTTPException(404, "No result yet")
    if not os.path.exists(r.json_path):
        raise HTTPException(500, "Result file missing on disk")
    return FileResponse(r.json_path, media_type="application/json", filename=f"{doc_id}.json")