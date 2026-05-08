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
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
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

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    source_type = Column(String, nullable=False)   # "knowledge_document" or "competitor_scrape"
    source_id = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    keyword = Column(String, nullable=False)
    meta_title = Column(Text, nullable=True)
    meta_description = Column(Text, nullable=True)
    intro = Column(Text, nullable=True)
    cta = Column(Text, nullable=True)
    draft_json = Column(Text, nullable=False)


class BlogVersion(Base):
    __tablename__ = "blog_versions"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)
    version_label = Column(String, nullable=False)
    draft_json = Column(Text, nullable=False)