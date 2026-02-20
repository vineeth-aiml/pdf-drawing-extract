import os
import pypdfium2 as pdfium
from app.core.config import settings
from app.services.pipeline.base import Stage

class RenderPagesStage(Stage):
    name = "render_pages"

    def run(self, ctx):
        os.makedirs(ctx.doc_dir, exist_ok=True)
        out_dir = os.path.join(ctx.doc_dir, "pages")
        os.makedirs(out_dir, exist_ok=True)

        pdf = pdfium.PdfDocument(ctx.pdf_path)
        dpi = int(settings.render_dpi)
        scale = dpi / 72.0

        ctx.page_images = []
        for i in range(len(pdf)):
            page = pdf[i]
            pil_image = page.render(scale=scale).to_pil()
            path = os.path.join(out_dir, f"page_{i:04d}.png")
            pil_image.save(path)
            ctx.page_images.append(path)
        return ctx
