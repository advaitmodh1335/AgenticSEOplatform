from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Project, CompetitorScrape, KnowledgeDocument
import json

router = APIRouter(prefix="/strategy", tags=["strategy"])


class TopicSuggestionRequest(BaseModel):
    project_id: int


@router.post("/topics")
def suggest_topics(data: TopicSuggestionRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        return {"topics": [], "message": "Project not found"}

    seed_keywords = project.seed_keywords.split(",") if project.seed_keywords else []

    scrapes = db.query(CompetitorScrape).filter(
        CompetitorScrape.project_id == data.project_id
    ).all()

    documents = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.project_id == data.project_id
    ).all()

    topics = []

    for keyword in seed_keywords:
        keyword = keyword.strip()
        if keyword:
            topics.append({
                "title": f"How {keyword} helps startup founders grow organic traffic",
                "keyword": keyword,
                "reason": "Derived from project seed keywords",
            })
            topics.append({
                "title": f"Best practices for {keyword} in 2026",
                "keyword": keyword,
                "reason": "SEO-focused educational topic",
            })

    for scrape in scrapes[:3]:
        topics.append({
            "title": f"What marketers can learn from {scrape.title}",
            "keyword": project.niche,
            "reason": "Inspired by competitor content",
        })

    return {"topics": topics[:10]}