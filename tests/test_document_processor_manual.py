from app.processing.document_processor import DocumentProcessor
from app.processing.ocr import OCRService
from app.processing.pdf_extractor import PDFTextExtractor


processor = DocumentProcessor(
    pdf_extractor=PDFTextExtractor(),
    ocr_service=OCRService(),
)

result = processor.process(
    "documents/factura_escaneada_prueba.pdf"
)

print("=" * 80)
print(f"Pages: {result.page_count}")
print(f"Extraction method: {result.extraction_method}")
print(f"Characters: {len(result.text)}")
print("=" * 80)
print(result.text[:3000])