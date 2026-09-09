from app.processing.ocr import OCRService

ocr_service = OCRService()

result = ocr_service.extract(
    "documents/f43de838-559a-4a9b-ba71-ea4649c56617.pdf"
)

print("=" * 80)
print(f"Pages: {result.page_count}")
print(f"Characters recognized: {len(result.text)}")
print("=" * 80)
print(result.text[:3000])