import os, json
from app.core.config import settings
from app.services.pipeline.context import ExtractionContext
from app.services.pipeline.pipelines import PIPELINES
from app.services.pipeline.registry import StageRegistry

def run_pipeline_sync(doc_id: str, pipeline_name: str) -> str:
    if pipeline_name not in PIPELINES:
        raise ValueError(f"Unknown pipeline: {pipeline_name}. Options: {list(PIPELINES.keys())}")

    doc_dir = os.path.join(settings.storage_dir, doc_id)
    pdf_path = os.path.join(doc_dir, "input.pdf")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Missing PDF for doc_id={doc_id}")

    ctx = ExtractionContext(doc_id=doc_id, pdf_path=pdf_path, doc_dir=doc_dir)
    registry = StageRegistry.default()
    for stage_name in PIPELINES[pipeline_name]:
        ctx = registry.get(stage_name).run(ctx)

    out_path = os.path.join(doc_dir, "result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ctx.to_dict(), f, ensure_ascii=False, indent=2)
    return out_path
