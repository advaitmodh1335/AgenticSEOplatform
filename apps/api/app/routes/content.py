from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Project
from app.services.vector_store import load_index, search_index
from app.services.embeddings import embed_query

router = APIRouter(prefix="/content", tags=["content"])


class OutlineRequest(BaseModel):
    project_id: int
    topic: str
    keyword: str

class DraftRequest(BaseModel):
    project_id: int
    topic: str
    keyword: str
    outline: dict

@router.post("/outline")
def generate_outline(data: OutlineRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        return {"message": "Project not found", "outline": None}

    index, metadata = load_index()

    retrieved_chunks = []
    if index is not None:
        query_text = f"{data.topic}. Keyword: {data.keyword}. Audience: {project.target_audience}"
        query_vector = embed_query(query_text)
        retrieved_chunks = search_index(index, query_vector, metadata, top_k=5)

    context_text = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    ) if retrieved_chunks else "No retrieved context available."

    outline = {
        "title": f"{data.topic}",
        "meta_title": f"{data.topic} | {project.name}",
        "meta_description": f"Learn about {data.keyword} with practical strategies for {project.target_audience}.",
        "intro": f"Introduce why {data.keyword} matters for {project.target_audience} and what the article will cover.",
        "sections": [
            f"What is {data.keyword}?",
            f"Why {data.keyword} matters for {project.target_audience}",
            f"Best practices for {data.keyword}",
            f"Common mistakes to avoid with {data.keyword}",
            f"How to apply {data.keyword} in a real workflow",
        ],
        "faq": [
            f"What is {data.keyword}?",
            f"Why is {data.keyword} important?",
            f"How can beginners improve {data.keyword}?",
        ],
        "cta": f"Encourage readers to apply these {data.keyword} strategies or explore your platform further.",
        "retrieved_context": retrieved_chunks,
        "project_name": project.name,
        "audience": project.target_audience,
        "niche": project.niche,
    }

    return {"outline": outline}

@router.post("/draft")
def generate_draft(data: DraftRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        return {"message": "Project not found", "draft": None}

    index, metadata = load_index()

    retrieved_chunks = []
    if index is not None:
        query_text = f"{data.topic}. Keyword: {data.keyword}. Audience: {project.target_audience}"
        query_vector = embed_query(query_text)
        retrieved_chunks = search_index(index, query_vector, metadata, top_k=5)

    retrieved_text = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    ) if retrieved_chunks else "No retrieved context available."

    sections = data.outline.get("sections", [])
    faq_items = data.outline.get("faq", [])

    section_content = []
    for section in sections:
        section_content.append({
            "heading": section,
            "content": (
                f"{section} is an important part of {data.keyword} for {project.target_audience}. "
                f"This section explains practical ideas, common use cases, and how it connects to {project.niche}. "
                f"Relevant context: {retrieved_text[:300]}"
            )
        })

    faq_content = []
    for item in faq_items:
        faq_content.append({
            "question": item,
            "answer": (
                f"{item} can be answered by focusing on practical SEO strategy, audience needs, "
                f"and how {data.keyword} should be implemented in a structured content workflow."
            )
        })

    draft = {
        "title": data.outline.get("title", data.topic),
        "meta_title": data.outline.get("meta_title", f"{data.topic} | {project.name}"),
        "meta_description": data.outline.get(
            "meta_description",
            f"Learn how {data.keyword} helps {project.target_audience} improve SEO performance."
        ),
        "intro": (
            f"{data.keyword} is becoming increasingly important for {project.target_audience}. "
            f"In this article, we explore the main strategies, best practices, and practical steps "
            f"needed to apply it effectively in a modern SEO workflow."
        ),
        "sections": section_content,
        "faq": faq_content,
        "cta": data.outline.get(
            "cta",
            f"Start applying these {data.keyword} strategies to improve your content and SEO results."
        ),
        "retrieved_context": retrieved_chunks,
        "project_name": project.name,
        "audience": project.target_audience,
        "niche": project.niche,
    }

    return {"draft": draft}