from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    target_audience = Column(String, nullable=False)
    seed_keywords = Column(Text, nullable=False)


class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)


class CompetitorScrape(Base):
    __tablename__ = "competitor_scrapes"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    meta_description = Column(Text, nullable=True)
    headings = Column(Text, nullable=True)
    content_preview = Column(Text, nullable=True)

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)