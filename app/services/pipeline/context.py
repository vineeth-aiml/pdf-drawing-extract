from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class ExtractionContext:
    doc_id: str
    pdf_path: str
    doc_dir: str

    page_types: List[str] = field(default_factory=list)
    page_images: List[str] = field(default_factory=list)

    vector_text: List[List[Dict[str, Any]]] = field(default_factory=list)
    ocr_text: List[List[Dict[str, Any]]] = field(default_factory=list)

    dimensions: List[List[Dict[str, Any]]] = field(default_factory=list)
    geometry: List[List[Dict[str, Any]]] = field(default_factory=list)

    meta: Dict[str, Any] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_count = self.meta.get("page_count") or max(
            len(self.page_types),
            len(self.page_images),
            len(self.vector_text),
            len(self.ocr_text),
            len(self.dimensions),
            len(self.geometry),
            1,
        )
        pages = []
        for i in range(page_count):
            pages.append({
                "page_index": i,
                "page_type": self.page_types[i] if i < len(self.page_types) else None,
                "image_path": self.page_images[i] if i < len(self.page_images) else None,
                "vector_text": self.vector_text[i] if i < len(self.vector_text) else [],
                "ocr_text": self.ocr_text[i] if i < len(self.ocr_text) else [],
                "dimensions": self.dimensions[i] if i < len(self.dimensions) else [],
                "geometry": self.geometry[i] if i < len(self.geometry) else [],
            })
        return {"doc_id": self.doc_id, "pdf_path": self.pdf_path, "meta": self.meta, "pages": pages, "artifacts": self.artifacts}
