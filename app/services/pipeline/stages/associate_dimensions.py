import math
from app.services.pipeline.base import Stage

def _center(b):
    x0,y0,x1,y1 = b
    return ((x0+x1)/2.0, (y0+y1)/2.0)

def _dist(p, q):
    return math.hypot(p[0]-q[0], p[1]-q[1])

class AssociateDimensionsStage(Stage):
    name = "associate_dimensions"

    def run(self, ctx):
        if not ctx.dimensions or not ctx.geometry:
            return ctx
        for i in range(min(len(ctx.dimensions), len(ctx.geometry))):
            lines = [g for g in ctx.geometry[i] if g.get("type") in ("raster_line","line")]
            if not lines:
                continue
            for dim in ctx.dimensions[i]:
                bb = dim.get("bbox")
                if not bb:
                    continue
                c = _center(bb)
                best = None
                best_d = 1e18
                for ln in lines:
                    p1, p2 = ln.get("p1"), ln.get("p2")
                    if not p1 or not p2:
                        continue
                    d = min(_dist(c, p1), _dist(c, p2))
                    if d < best_d:
                        best_d, best = d, ln
                if best and best_d < 250:
                    dim["associated_line"] = {"p1": best.get("p1"), "p2": best.get("p2"), "type": best.get("type")}
                    dim["association_distance_px"] = float(best_d)
        return ctx
