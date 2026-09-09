from pathlib import Path

from app.processing.pdf_extractor import PDFTextExtractor

PDF_PATH = Path(
    "documents/f43de838-559a-4a9b-ba71-ea4649c56617.pdf"
)


def test_pdf_text_extraction():
    extractor = PDFTextExtractor()

    result = extractor.extract(str(PDF_PATH))

    assert result.page_count == 2
    assert result.has_text is True
    assert len(result.text) > 0
