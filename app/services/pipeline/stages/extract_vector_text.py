import fitz
from app.services.pipeline.base import Stage

class ExtractVectorTextStage(Stage):
    name = "extract_vector_text"

    def run(self, ctx):
        doc = fitz.open(ctx.pdf_path)
        ctx.vector_text = []
        for i in range(doc.page_count):
            page = doc.load_page(i)
            blocks = []
            if ctx.page_types and ctx.page_types[i] == "VECTOR":
                raw = page.get_text("blocks")
                for (x0, y0, x1, y1, text, *_rest) in raw:
                    t = (text or "").strip()
                    if not t:
                        continue
                    blocks.append({"text": t, "bbox": [float(x0), float(y0), float(x1), float(y1)], "source": "vector", "confidence": 1.0})
            ctx.vector_text.append(blocks)
        doc.close()
        return ctx
