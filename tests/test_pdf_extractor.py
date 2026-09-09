import pymupdf

from app.processing.pdf_extractor import PDFTextExtractor


def test_pdf_text_extraction(tmp_path):
    pdf_path = tmp_path / "test_document.pdf"

    document = pymupdf.open()

    try:
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Documento de prueba para PDF extraction",
        )

        document.save(pdf_path)

    finally:
        document.close()

    extractor = PDFTextExtractor()

    result = extractor.extract(str(pdf_path))

    assert result.page_count == 1
    assert result.has_text is True
    assert "Documento de prueba" in result.text