from typing import Dict
from app.services.pipeline.base import Stage
from app.services.pipeline.stages import (
    DetectPdfTypeStage,
    RenderPagesStage,
    ExtractVectorTextStage,
    ExtractVectorGeometryStage,
    OcrPagesStage,
    ParseDimensionsStage,
    DetectRasterGeometryStage,
    AssociateDimensionsStage,
)

class StageRegistry:
    def __init__(self):
        self._stages: Dict[str, Stage] = {}

    def register(self, stage: Stage):
        self._stages[stage.name] = stage

    def get(self, name: str) -> Stage:
        if name not in self._stages:
            raise KeyError(f"Stage not registered: {name}")
        return self._stages[name]

    @classmethod
    def default(cls) -> "StageRegistry":
        r = cls()
        for s in [
            DetectPdfTypeStage(),
            RenderPagesStage(),
            ExtractVectorTextStage(),
            ExtractVectorGeometryStage(),
            OcrPagesStage(),
            ParseDimensionsStage(),
            DetectRasterGeometryStage(),
            AssociateDimensionsStage(),
        ]:
            r.register(s)
        return r
