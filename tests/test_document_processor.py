from unittest.mock import Mock

from app.processing.document_processor import DocumentProcessor
from app.processing.ocr import OCRResult
from app.processing.pdf_extractor import PDFExtractionResult


def test_processor_uses_pdf_text_when_available():
    pdf_extractor = Mock()
    ocr_service = Mock()

    pdf_extractor.extract.return_value = PDFExtractionResult(
        text="Texto extraído del PDF",
        page_count=2,
        has_text=True,
    )

    processor = DocumentProcessor(
        pdf_extractor=pdf_extractor,
        ocr_service=ocr_service,
    )

    result = processor.process("document.pdf")

    assert result.text == "Texto extraído del PDF"
    assert result.page_count == 2
    assert result.extraction_method == "pdf_text"

    ocr_service.extract.assert_not_called()


def test_processor_uses_ocr_when_pdf_has_no_text():
    pdf_extractor = Mock()
    ocr_service = Mock()

    pdf_extractor.extract.return_value = PDFExtractionResult(
        text="",
        page_count=3,
        has_text=False,
    )

    ocr_service.extract.return_value = OCRResult(
        text="Texto obtenido mediante OCR",
        page_count=3,
    )

    processor = DocumentProcessor(
        pdf_extractor=pdf_extractor,
        ocr_service=ocr_service,
    )

    result = processor.process("scanned_document.pdf")

    assert result.text == "Texto obtenido mediante OCR"
    assert result.page_count == 3
    assert result.extraction_method == "ocr"

    ocr_service.extract.assert_called_once_with(
        "scanned_document.pdf"
    )
