from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import KnowledgeDocument

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    project_id: int
    title: str
    doc_type: str
    content: str


@router.post("")
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = KnowledgeDocument(
        project_id=document.project_id,
        title=document.title,
        doc_type=document.doc_type,
        content=document.content,
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "id": new_document.id,
        "project_id": new_document.project_id,
        "title": new_document.title,
        "doc_type": new_document.doc_type,
        "content": new_document.content,
    }


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(KnowledgeDocument).all()

    return [
        {
            "id": document.id,
            "project_id": document.project_id,
            "title": document.title,
            "doc_type": document.doc_type,
            "content": document.content,
        }
        for document in documents
    ]