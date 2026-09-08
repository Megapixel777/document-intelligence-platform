from dataclasses import dataclass

import pymupdf


@dataclass
class PDFExtractionResult:
    text: str
    page_count: int
    has_text: bool


class PDFTextExtractor:

    def extract(self, file_path: str) -> PDFExtractionResult:
        document = pymupdf.open(file_path)

        try:
            pages_text = []

            for page in document:
                text = page.get_text()
                pages_text.append(text)

            full_text = "\n".join(pages_text).strip()

            return PDFExtractionResult(
                text=full_text,
                page_count=len(document),
                has_text=bool(full_text),
            )

        finally:
            document.close()