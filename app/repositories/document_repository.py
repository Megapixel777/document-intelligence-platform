from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    def create(
        self,
        db: Session,
        document: Document,
    ) -> Document:
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def get_by_id(
        self,
        db: Session,
        document_id: UUID,
    ) -> Document | None:
        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        status: str | None = None,
    ) -> list[Document]:
        query = db.query(Document)

        if status is not None:
            query = query.filter(Document.status == status)

        return (
            query
            .order_by(Document.created_at.desc())
            .all()
        )

    def get_for_review(
        self,
        db: Session,
    ) -> list[Document]:
        return (
            db.query(Document)
            .filter(Document.status == "needs_review")
            .order_by(Document.created_at.asc())
            .all()
        )

    def update(
        self,
        db: Session,
        document: Document,
    ) -> Document:
        db.commit()
        db.refresh(document)

        return document
