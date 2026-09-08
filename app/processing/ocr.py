from dataclasses import dataclass
from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image


@dataclass
class OCRResult:
    text: str
    page_count: int


class OCRService:

    def extract(self, file_path: str) -> OCRResult:
        document = pymupdf.open(file_path)

        try:
            pages_text = []

            for page in document:
                pixmap = page.get_pixmap(dpi=200)

                image = Image.open(
                    BytesIO(pixmap.tobytes("png"))
                )

                text = pytesseract.image_to_string(
                    image,
                    lang="spa+eng",
                )

                pages_text.append(text)

            full_text = "\n".join(pages_text).strip()

            return OCRResult(
                text=full_text,
                page_count=len(document),
            )

        finally:
            document.close()