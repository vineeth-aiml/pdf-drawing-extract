from abc import ABC, abstractmethod
from app.services.pipeline.context import ExtractionContext

class Stage(ABC):
    name: str = "stage"

    @abstractmethod
    def run(self, ctx: ExtractionContext) -> ExtractionContext:
        raise NotImplementedError
