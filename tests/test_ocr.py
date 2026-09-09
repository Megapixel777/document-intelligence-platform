from pathlib import Path

from app.processing.ocr import OCRService

PDF_PATH = Path(
    "documents/factura_escaneada_prueba.pdf"
)


def test_ocr_extracts_text_from_scanned_pdf():
    ocr_service = OCRService()

    result = ocr_service.extract(str(PDF_PATH))

    assert result.page_count == 1
    assert len(result.text) > 0
    assert "FACTURA" in result.text.upper()
