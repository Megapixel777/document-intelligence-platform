from dataclasses import dataclass

from app.processing.ocr import OCRService
from app.processing.pdf_extractor import PDFTextExtractor


@dataclass
class DocumentProcessingResult:
    text: str
    page_count: int
    extraction_method: str


class DocumentProcessor:

    def __init__(
        self,
        pdf_extractor: PDFTextExtractor,
        ocr_service: OCRService,
    ):
        self.pdf_extractor = pdf_extractor
        self.ocr_service = ocr_service

    def process(self, file_path: str) -> DocumentProcessingResult:
        pdf_result = self.pdf_extractor.extract(file_path)

        if pdf_result.has_text:
            return DocumentProcessingResult(
                text=pdf_result.text,
                page_count=pdf_result.page_count,
                extraction_method="pdf_text",
            )

        ocr_result = self.ocr_service.extract(file_path)

        return DocumentProcessingResult(
            text=ocr_result.text,
            page_count=ocr_result.page_count,
            extraction_method="ocr",
        )