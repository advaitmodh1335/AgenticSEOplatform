from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, projects, competitors, documents, rag, strategy, content, seo, links, headlines, images, blogs
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic SEO Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.110:3000",
        "https://your-vercel-project.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(competitors.router)
app.include_router(documents.router)
app.include_router(rag.router)
app.include_router(strategy.router)
app.include_router(content.router)
app.include_router(seo.router)
app.include_router(links.router)
app.include_router(headlines.router)
app.include_router(images.router)
app.include_router(blogs.router)