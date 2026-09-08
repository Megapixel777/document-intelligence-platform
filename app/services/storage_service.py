from pathlib import Path
from uuid import UUID

from fastapi import UploadFile


class StorageService:

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_document(self, document_id: UUID, file: UploadFile) -> str:
        file_extension = Path(file.filename or "").suffix.lower()

        file_path = self.base_path / f"{document_id}{file_extension}"

        content = await file.read()

        file_path.write_bytes(content)

        return str(file_path)