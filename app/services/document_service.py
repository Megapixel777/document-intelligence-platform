import uuid

from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.services.storage_service import StorageService


class DocumentService:

    def __init__(
        self,
        storage_service: StorageService,
        document_repository: DocumentRepository,
    ):
        self.storage_service = storage_service
        self.document_repository = document_repository

    async def upload_document(
        self,
        db: Session,
        file: UploadFile,
    ) -> Document:

        document_id = uuid.uuid4()

        document = Document(
            id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            file_size=0,
            file_path="",
            status="uploaded",
        )

        file_path = await self.storage_service.save_document(
            document_id=document_id,
            file=file,
        )

        document.file_path = file_path

        with open(file_path, "rb") as stored_file:
            document.file_size = len(stored_file.read())

        return self.document_repository.create(
            db=db,
            document=document,
        )