from app.processing.pdf_extractor import PDFTextExtractor


extractor = PDFTextExtractor()

result = extractor.extract(
    "documents/f43de838-559a-4a9b-ba71-ea4649c56617.pdf"
)

print("=" * 80)
print(f"Pages: {result.page_count}")
print(f"Has text: {result.has_text}")
print(f"Characters extracted: {len(result.text)}")
print("=" * 80)
print(result.text[:3000])