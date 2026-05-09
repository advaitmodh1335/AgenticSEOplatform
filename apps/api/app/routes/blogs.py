import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Blog, BlogVersion

router = APIRouter(prefix="/blogs", tags=["blogs"])


class BlogCreate(BaseModel):
    project_id: int
    title: str
    keyword: str
    meta_title: str | None = None
    meta_description: str | None = None
    intro: str | None = None
    cta: str | None = None
    draft: dict
    selected_headline: str | None = None
    selected_image_prompt: str | None = None
    selected_image_concept_name: str | None = None
    selected_image_style: str | None = None
    selected_image_aspect_ratio: str | None = None


class BlogVersionCreate(BaseModel):
    blog_id: int
    version_label: str
    draft: dict

class BlogUpdateSelections(BaseModel):
    selected_headline: str | None = None
    selected_image_prompt: str | None = None
    selected_image_concept_name: str | None = None
    selected_image_style: str | None = None
    selected_image_aspect_ratio: str | None = None

@router.post("")
def create_blog(data: BlogCreate, db: Session = Depends(get_db)):
    new_blog = Blog(
        project_id=data.project_id,
        title=data.title,
        keyword=data.keyword,
        meta_title=data.meta_title,
        meta_description=data.meta_description,
        intro=data.intro,
        cta=data.cta,
        draft_json=json.dumps(data.draft),
        selected_headline=data.selected_headline,
        selected_image_prompt=data.selected_image_prompt,
        selected_image_concept_name=data.selected_image_concept_name,
        selected_image_style=data.selected_image_style,
        selected_image_aspect_ratio=data.selected_image_aspect_ratio,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    initial_version = BlogVersion(
        blog_id=new_blog.id,
        version_label="initial_draft",
        draft_json=json.dumps(data.draft),
    )
    db.add(initial_version)
    db.commit()

    return {
        "id": new_blog.id,
        "project_id": new_blog.project_id,
        "title": new_blog.title,
        "keyword": new_blog.keyword,
        "meta_title": new_blog.meta_title,
        "meta_description": new_blog.meta_description,
        "intro": new_blog.intro,
        "cta": new_blog.cta,
        "draft": data.draft,
        "selected_headline": new_blog.selected_headline,
        "selected_image_prompt": new_blog.selected_image_prompt,
        "selected_image_concept_name": new_blog.selected_image_concept_name,
        "selected_image_style": new_blog.selected_image_style,
        "selected_image_aspect_ratio": new_blog.selected_image_aspect_ratio,
    }


@router.get("")
def list_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()

    return [
        {
            "id": blog.id,
            "project_id": blog.project_id,
            "title": blog.title,
            "keyword": blog.keyword,
            "meta_title": blog.meta_title,
            "meta_description": blog.meta_description,
        }
        for blog in blogs
    ]


@router.get("/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        return {"message": "Blog not found"}

    return {
        "id": blog.id,
        "project_id": blog.project_id,
        "title": blog.title,
        "keyword": blog.keyword,
        "meta_title": blog.meta_title,
        "meta_description": blog.meta_description,
        "intro": blog.intro,
        "cta": blog.cta,
        "draft": json.loads(blog.draft_json),
        "selected_headline": blog.selected_headline,
        "selected_image_prompt": blog.selected_image_prompt,
        "selected_image_concept_name": blog.selected_image_concept_name,
        "selected_image_style": blog.selected_image_style,
        "selected_image_aspect_ratio": blog.selected_image_aspect_ratio,
    }


@router.post("/version")
def create_blog_version(data: BlogVersionCreate, db: Session = Depends(get_db)):
    new_version = BlogVersion(
        blog_id=data.blog_id,
        version_label=data.version_label,
        draft_json=json.dumps(data.draft),
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    return {
        "id": new_version.id,
        "blog_id": new_version.blog_id,
        "version_label": new_version.version_label,
        "draft": data.draft,
    }


@router.get("/{blog_id}/versions")
def list_blog_versions(blog_id: int, db: Session = Depends(get_db)):
    versions = (
        db.query(BlogVersion)
        .filter(BlogVersion.blog_id == blog_id)
        .order_by(BlogVersion.id.desc())
        .all()
    )

    return [
        {
            "id": version.id,
            "blog_id": version.blog_id,
            "version_label": version.version_label,
            "draft": json.loads(version.draft_json),
        }
        for version in versions
    ]

@router.put("/{blog_id}/selections")
def update_blog_selections(blog_id: int, data: BlogUpdateSelections, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        return {"message": "Blog not found"}

    blog.selected_headline = data.selected_headline
    blog.selected_image_prompt = data.selected_image_prompt
    blog.selected_image_concept_name = data.selected_image_concept_name
    blog.selected_image_style = data.selected_image_style
    blog.selected_image_aspect_ratio = data.selected_image_aspect_ratio

    db.commit()
    db.refresh(blog)

    return {
        "id": blog.id,
        "selected_headline": blog.selected_headline,
        "selected_image_prompt": blog.selected_image_prompt,
        "selected_image_concept_name": blog.selected_image_concept_name,
        "selected_image_style": blog.selected_image_style,
        "selected_image_aspect_ratio": blog.selected_image_aspect_ratio,
    }