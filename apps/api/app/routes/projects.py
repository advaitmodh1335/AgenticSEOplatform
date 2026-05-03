from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/projects", tags=["projects"])

projects_db = []

class ProjectCreate(BaseModel):
    name: str
    niche: str
    target_audience: str
    seed_keywords: List[str]

@router.post("")
def create_project(project: ProjectCreate):
    new_project = {
        "id": len(projects_db) + 1,
        "name": project.name,
        "niche": project.niche,
        "target_audience": project.target_audience,
        "seed_keywords": project.seed_keywords,
    }
    projects_db.append(new_project)
    return new_project

@router.get("")
def list_projects():
    return projects_db