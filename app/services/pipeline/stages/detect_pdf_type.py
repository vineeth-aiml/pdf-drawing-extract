import fitz
from app.services.pipeline.base import Stage

class DetectPdfTypeStage(Stage):
    name = "detect_pdf_type"

    def run(self, ctx):
        doc = fitz.open(ctx.pdf_path)
        ctx.page_types = []
        for i in range(doc.page_count):
            page = doc.load_page(i)
            text = page.get_text("text").strip()
            drawings = page.get_drawings()
            if text or (drawings and len(drawings) > 15):
                ctx.page_types.append("VECTOR")
            else:
                ctx.page_types.append("RASTER")
        ctx.meta["page_count"] = doc.page_count
        doc.close()
        return ctx
