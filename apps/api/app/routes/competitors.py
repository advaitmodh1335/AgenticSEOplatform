from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.scraper import scrape_url

router = APIRouter(prefix="/competitors", tags=["competitors"])

competitors_db = []


class CompetitorCreate(BaseModel):
    project_id: int
    name: str
    url: str


class ScrapeRequest(BaseModel):
    url: str


@router.post("")
def create_competitor(competitor: CompetitorCreate):
    new_competitor = {
        "id": len(competitors_db) + 1,
        "project_id": competitor.project_id,
        "name": competitor.name,
        "url": competitor.url,
    }
    competitors_db.append(new_competitor)
    return new_competitor


@router.get("")
def list_competitors():
    return competitors_db


@router.post("/scrape")
def scrape_competitor(data: ScrapeRequest):
    try:
        return scrape_url(data.url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))