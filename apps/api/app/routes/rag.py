from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import KnowledgeDocument, CompetitorScrape, DocumentChunk
from app.services.chunker import chunk_text
from app.services.embeddings import embed_texts, embed_query
from app.services.vector_store import create_index, save_index, load_index, search_index
import json

router = APIRouter(prefix="/rag", tags=["rag"])


class IndexRequest(BaseModel):
    project_id: int


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/index")
def build_index(data: IndexRequest, db: Session = Depends(get_db)):
    db.query(DocumentChunk).filter(DocumentChunk.project_id == data.project_id).delete()
    db.commit()

    texts = []
    metadata = []

    documents = db.query(KnowledgeDocument).filter(KnowledgeDocument.project_id == data.project_id).all()
    for doc in documents:
        chunks = chunk_text(doc.content)
        for chunk in chunks:
            chunk_row = DocumentChunk(
                project_id=data.project_id,
                source_type="knowledge_document",
                source_id=doc.id,
                chunk_text=chunk,
            )
            db.add(chunk_row)
            db.flush()

            texts.append(chunk)
            metadata.append({
                "chunk_id": chunk_row.id,
                "source_type": "knowledge_document",
                "source_id": doc.id,
                "text": chunk,
                "title": doc.title,
            })

    scrapes = db.query(CompetitorScrape).all()
    for scrape in scrapes:
        combined_text = " ".join([
            scrape.title or "",
            scrape.meta_description or "",
            " ".join(json.loads(scrape.headings) if scrape.headings else []),
            " ".join(json.loads(scrape.content_preview) if scrape.content_preview else []),
        ]).strip()

        chunks = chunk_text(combined_text)
        for chunk in chunks:
            chunk_row = DocumentChunk(
                project_id=data.project_id,
                source_type="competitor_scrape",
                source_id=scrape.id,
                chunk_text=chunk,
            )
            db.add(chunk_row)
            db.flush()

            texts.append(chunk)
            metadata.append({
                "chunk_id": chunk_row.id,
                "source_type": "competitor_scrape",
                "source_id": scrape.id,
                "text": chunk,
                "title": scrape.title,
            })

    db.commit()

    if not texts:
        return {"message": "No content found to index", "count": 0}

    embeddings = embed_texts(texts)
    dimension = embeddings.shape[1]
    index = create_index(dimension)
    index.add(embeddings)

    save_index(index, metadata)

    return {
        "message": "Index built successfully",
        "count": len(texts),
    }


@router.post("/query")
def query_index(data: QueryRequest):
    index, metadata = load_index()

    if index is None:
        return {"results": [], "message": "No index found. Build the index first."}

    query_vector = embed_query(data.query)
    results = search_index(index, query_vector, metadata, top_k=data.top_k)

    return {"results": results}