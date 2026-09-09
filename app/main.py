from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes.documents import router as documents_router
from app.core.database import engine

app = FastAPI(
    title="Document Intelligence Platform",
    description="API for automated document processing and information extraction.",
    version="0.1.0",
)

@app.get("/")
def root(): return { "application": "Document Intelligence Platform",
                     "version": "0.1.0", "status": "running",
                     "documentation": "/docs", }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "database": "healthy",
        "result": value,
    }

app.include_router(documents_router)