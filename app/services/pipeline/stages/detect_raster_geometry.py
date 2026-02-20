import cv2
import numpy as np
from app.services.pipeline.base import Stage

class DetectRasterGeometryStage(Stage):
    name = "detect_raster_geometry"

    def run(self, ctx):
        if not ctx.page_images:
            return ctx
        page_count = len(ctx.page_images)
        if not ctx.geometry:
            ctx.geometry = [[] for _ in range(page_count)]
        while len(ctx.geometry) < page_count:
            ctx.geometry.append([])

        for i, img_path in enumerate(ctx.page_images):
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            blur = cv2.GaussianBlur(img, (3,3), 0)
            edges = cv2.Canny(blur, 50, 150, apertureSize=3)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=120, minLineLength=80, maxLineGap=10)
            if lines is None:
                continue
            prim = []
            for x1,y1,x2,y2 in lines[:,0]:
                length = float(np.hypot(x2-x1, y2-y1))
                if length < 80:
                    continue
                prim.append({"type": "raster_line", "p1": [float(x1), float(y1)], "p2": [float(x2), float(y2)], "length": length})
            if len(prim) > 5000:
                prim = prim[:5000]
            ctx.geometry[i].extend(prim)
        return ctx
