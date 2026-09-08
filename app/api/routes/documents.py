from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.database import SessionLocal
from app.core.config import settings
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.services.storage_service import StorageService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


storage_service = StorageService(settings.documents_path)
document_repository = DocumentRepository()

document_service = DocumentService(
    storage_service=storage_service,
    document_repository=document_repository,
)


@router.post("/")
async def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    db = SessionLocal()

    try:
        document = await document_service.upload_document(
            db=db,
            file=file,
        )

        return {
            "document_id": str(document.id),
            "filename": document.filename,
            "content_type": document.content_type,
            "file_size": document.file_size,
            "file_path": document.file_path,
            "status": document.status,
        }

    finally:
        db.close()