from typing import List, Dict, Any
from app.core.config import settings
from app.services.pipeline.base import Stage

def _has_paddle():
    try:
        import paddleocr  # noqa
        return True
    except Exception:
        return False

class OcrPagesStage(Stage):
    name = "ocr_pages"

    def __init__(self):
        self._ocr = None

    def _init(self):
        if settings.ocr_engine == "none":
            return None
        if settings.ocr_engine == "paddle":
            if not _has_paddle():
                raise RuntimeError("OCR_ENGINE=paddle but PaddleOCR not installed/working. Set OCR_ENGINE=none or install paddle.")
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(use_angle_cls=True, lang="en")
            return self._ocr
        raise ValueError(f"Unknown OCR_ENGINE: {settings.ocr_engine}")

    def run(self, ctx):
        if settings.ocr_engine == "none":
            ctx.ocr_text = [[] for _ in ctx.page_images]
            return ctx

        ocr = self._ocr or self._init()
        out: List[List[Dict[str, Any]]] = []
        for img_path in ctx.page_images:
            res = ocr.ocr(img_path, cls=True) or []
            blocks = []
            for line in res:
                if not line:
                    continue
                for det in line if isinstance(line, list) else [line]:
                    if not det or len(det) < 2:
                        continue
                    box = det[0]
                    txt, conf = det[1][0], float(det[1][1])
                    xs = [p[0] for p in box]; ys = [p[1] for p in box]
                    bbox = [float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys))]
                    t = (txt or "").strip()
                    if t:
                        blocks.append({"text": t, "bbox": bbox, "source": "ocr", "confidence": conf})
            out.append(blocks)
        ctx.ocr_text = out
        return ctx
