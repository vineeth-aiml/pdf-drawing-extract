PIPELINES = {
    "v1": ["detect_pdf_type", "render_pages", "extract_vector_text", "ocr_pages"],
    "v2": ["detect_pdf_type", "render_pages", "extract_vector_text", "ocr_pages", "parse_dimensions"],
    "v3": ["detect_pdf_type", "render_pages", "extract_vector_text", "extract_vector_geometry", "ocr_pages", "parse_dimensions", "detect_raster_geometry", "associate_dimensions"],
    "final": ["detect_pdf_type", "render_pages", "extract_vector_text", "extract_vector_geometry", "ocr_pages", "parse_dimensions", "detect_raster_geometry", "associate_dimensions"],
}
