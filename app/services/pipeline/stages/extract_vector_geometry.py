import fitz
from app.services.pipeline.base import Stage

class ExtractVectorGeometryStage(Stage):
    name = "extract_vector_geometry"

    def run(self, ctx):
        doc = fitz.open(ctx.pdf_path)
        if not ctx.geometry:
            ctx.geometry = [[] for _ in range(doc.page_count)]
        while len(ctx.geometry) < doc.page_count:
            ctx.geometry.append([])

        for i in range(doc.page_count):
            if ctx.page_types and ctx.page_types[i] != "VECTOR":
                continue
            page = doc.load_page(i)
            drawings = page.get_drawings()
            primitives = []
            for d in drawings:
                for item in d.get("items", []):
                    op = item[0]
                    if op == "l":
                        p1, p2 = item[1], item[2]
                        primitives.append({"type": "line", "p1": [p1.x, p1.y], "p2": [p2.x, p2.y]})
                    elif op == "re":
                        r = item[1]
                        primitives.append({"type": "rect", "bbox": [r.x0, r.y0, r.x1, r.y1]})
                    elif op == "c":
                        p1, p2, p3, p4 = item[1], item[2], item[3], item[4]
                        primitives.append({"type": "bezier", "p1": [p1.x, p1.y], "c1": [p2.x, p2.y], "c2": [p3.x, p3.y], "p2": [p4.x, p4.y]})
            if len(primitives) > 20000:
                primitives = primitives[:20000]
            ctx.geometry[i].extend(primitives)
        doc.close()
        return ctx
