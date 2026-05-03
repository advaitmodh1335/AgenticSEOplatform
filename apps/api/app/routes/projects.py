from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    niche: str
    target_audience: str
    seed_keywords: List[str]


@router.post("")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        name=project.name,
        niche=project.niche,
        target_audience=project.target_audience,
        seed_keywords=",".join(project.seed_keywords),
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "id": new_project.id,
        "name": new_project.name,
        "niche": new_project.niche,
        "target_audience": new_project.target_audience,
        "seed_keywords": new_project.seed_keywords.split(",") if new_project.seed_keywords else [],
    }


@router.get("")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return [
        {
            "id": project.id,
            "name": project.name,
            "niche": project.niche,
            "target_audience": project.target_audience,
            "seed_keywords": project.seed_keywords.split(",") if project.seed_keywords else [],
        }
        for project in projects
    ]