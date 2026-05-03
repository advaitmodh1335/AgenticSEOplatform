import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Competitor, CompetitorScrape
from app.services.scraper import scrape_url

router = APIRouter(prefix="/competitors", tags=["competitors"])


class CompetitorCreate(BaseModel):
    project_id: int
    name: str
    url: str


class ScrapeRequest(BaseModel):
    url: str
    competitor_id: int | None = None


@router.post("")
def create_competitor(competitor: CompetitorCreate, db: Session = Depends(get_db)):
    new_competitor = Competitor(
        project_id=competitor.project_id,
        name=competitor.name,
        url=competitor.url,
    )
    db.add(new_competitor)
    db.commit()
    db.refresh(new_competitor)

    return {
        "id": new_competitor.id,
        "project_id": new_competitor.project_id,
        "name": new_competitor.name,
        "url": new_competitor.url,
    }


@router.get("")
def list_competitors(db: Session = Depends(get_db)):
    competitors = db.query(Competitor).all()

    return [
        {
            "id": competitor.id,
            "project_id": competitor.project_id,
            "name": competitor.name,
            "url": competitor.url,
        }
        for competitor in competitors
    ]


@router.post("/scrape")
def scrape_competitor(data: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraped = scrape_url(data.url)

        new_scrape = CompetitorScrape(
            competitor_id=data.competitor_id,
            url=scraped["url"],
            title=scraped["title"],
            meta_description=scraped["meta_description"],
            headings=json.dumps(scraped["headings"]),
            content_preview=json.dumps(scraped["content_preview"]),
        )

        db.add(new_scrape)
        db.commit()
        db.refresh(new_scrape)

        return {
            "id": new_scrape.id,
            "competitor_id": new_scrape.competitor_id,
            "url": new_scrape.url,
            "title": new_scrape.title,
            "meta_description": new_scrape.meta_description,
            "headings": scraped["headings"],
            "content_preview": scraped["content_preview"],
        }

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/scrapes")
def list_scrapes(db: Session = Depends(get_db)):
    scrapes = db.query(CompetitorScrape).all()

    return [
        {
            "id": scrape.id,
            "competitor_id": scrape.competitor_id,
            "url": scrape.url,
            "title": scrape.title,
            "meta_description": scrape.meta_description,
            "headings": json.loads(scrape.headings) if scrape.headings else [],
            "content_preview": json.loads(scrape.content_preview) if scrape.content_preview else [],
        }
        for scrape in scrapes
    ]