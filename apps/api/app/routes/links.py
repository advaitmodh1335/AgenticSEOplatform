from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import KnowledgeDocument, CompetitorScrape

router = APIRouter(prefix="/links", tags=["links"])


class LinkSuggestionRequest(BaseModel):
    project_id: int
    keyword: str
    draft: dict


@router.post("/suggest")
def suggest_internal_links(data: LinkSuggestionRequest, db: Session = Depends(get_db)):
    keyword = data.keyword.lower().strip()
    draft = data.draft

    draft_text_parts = [
        draft.get("title", ""),
        draft.get("meta_title", ""),
        draft.get("meta_description", ""),
        draft.get("intro", ""),
        draft.get("cta", ""),
    ]

    for section in draft.get("sections", []):
        draft_text_parts.append(section.get("heading", ""))
        draft_text_parts.append(section.get("content", ""))

    draft_text = " ".join(draft_text_parts).lower()

    suggestions = []

    documents = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.project_id == data.project_id
    ).all()

    for doc in documents:
        content_lower = (doc.content or "").lower()
        score = 0

        if keyword and keyword in content_lower:
            score += 2

        title_words = doc.title.lower().split()
        overlap = sum(1 for word in title_words if word in draft_text)
        score += overlap

        if score > 0:
            anchor_text = keyword if keyword else doc.title

            suggestions.append({
                "target_title": doc.title,
                "source_type": "knowledge_document",
                "source_id": doc.id,
                "anchor_text": anchor_text,
                "reason": f"Relevant because it overlaps with draft topic and keyword usage.",
                "score": score,
            })

    scrapes = db.query(CompetitorScrape).filter(
        CompetitorScrape.project_id == data.project_id
    ).all()

    for scrape in scrapes:
        title_lower = (scrape.title or "").lower()
        meta_lower = (scrape.meta_description or "").lower()
        combined = f"{title_lower} {meta_lower}"

        score = 0

        if keyword and keyword in combined:
            score += 2

        title_words = title_lower.split()
        overlap = sum(1 for word in title_words if word in draft_text)
        score += overlap

        if score > 0:
            anchor_text = keyword if keyword else scrape.title

            suggestions.append({
                "target_title": scrape.title,
                "source_type": "competitor_scrape",
                "source_id": scrape.id,
                "anchor_text": anchor_text,
                "reason": f"Relevant because the competitor content matches the article topic.",
                "score": score,
            })

    suggestions.sort(key=lambda item: item["score"], reverse=True)

    return {
        "suggestions": suggestions[:5]
    }