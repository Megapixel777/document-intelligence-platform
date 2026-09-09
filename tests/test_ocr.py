from io import BytesIO

import pymupdf
from PIL import Image, ImageDraw, ImageFont

from app.processing.ocr import OCRService


def test_ocr_extracts_text_from_scanned_pdf(tmp_path):
    image = Image.new(
        "RGB",
        (1600, 600),
        "white",
    )

    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default(size=64)

    draw.text(
        (100, 100),
        "FACTURA TEST",
        fill="black",
        font=font,
    )

    image_buffer = BytesIO()

    image.save(
        image_buffer,
        format="PNG",
    )

    image_buffer.seek(0)

    pdf_path = tmp_path / "scanned_test.pdf"

    document = pymupdf.open()

    try:
        page = document.new_page(
            width=1600,
            height=600,
        )

        page.insert_image(
            page.rect,
            stream=image_buffer.getvalue(),
        )

        document.save(pdf_path)

    finally:
        document.close()

    ocr_service = OCRService()

    result = ocr_service.extract(str(pdf_path))

    assert result.page_count == 1
    assert len(result.text) > 0
    assert "FACTURA" in result.text.upper()