import re
from app.services.pipeline.base import Stage

RE_DIAM = re.compile(r"(?:Ø|⌀|DIA)\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
RE_RAD  = re.compile(r"R\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
RE_ANG  = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*°")
RE_TOL1 = re.compile(r"±\s*([0-9]+(?:\.[0-9]+)?)")
RE_TOL2 = re.compile(r"\+([0-9]+(?:\.[0-9]+)?)\s*/\s*-([0-9]+(?:\.[0-9]+)?)")
RE_NUM  = re.compile(r"(?<![A-Za-z])([0-9]+(?:\.[0-9]+)?)\b")

def classify_dimension(text: str):
    t = text.strip()
    m = RE_DIAM.search(t)
    if m: return ("diameter", float(m.group(1)), t)
    m = RE_RAD.search(t)
    if m: return ("radius", float(m.group(1)), t)
    m = RE_ANG.search(t)
    if m: return ("angle", float(m.group(1)), t)
    m = RE_TOL1.search(t)
    if m: return ("tolerance_pm", float(m.group(1)), t)
    m = RE_TOL2.search(t)
    if m: return ("tolerance_plus_minus", (float(m.group(1)), float(m.group(2))), t)
    m = RE_NUM.search(t)
    if m and len(m.group(1)) <= 6:
        return ("linear_guess", float(m.group(1)), t)
    return (None, None, t)

class ParseDimensionsStage(Stage):
    name = "parse_dimensions"

    def run(self, ctx):
        page_count = ctx.meta.get("page_count", max(len(ctx.vector_text), len(ctx.ocr_text), 0))
        ctx.dimensions = [[] for _ in range(page_count)]

        for i in range(page_count):
            candidates = []
            if i < len(ctx.vector_text): candidates.extend(ctx.vector_text[i])
            if i < len(ctx.ocr_text): candidates.extend(ctx.ocr_text[i])

            dims = []
            for blk in candidates:
                kind, value, raw = classify_dimension(blk["text"])
                if not kind: 
                    continue
                dims.append({
                    "kind": kind,
                    "value": value,
                    "raw": raw,
                    "bbox": blk.get("bbox"),
                    "source": blk.get("source"),
                    "confidence": float(blk.get("confidence", 0.5)),
                })
            ctx.dimensions[i] = dims
        return ctx
