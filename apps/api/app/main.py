from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, projects, competitors

app = FastAPI(title="Agentic SEO Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(competitors.router)