import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes_projects import router as projects_router
from app.api.routes_claims import router as claims_router
from app.api.routes_content import router as content_router
from app.api.routes_artifacts import router as artifacts_router
from app.api.routes_export import router as export_router
from app.api.routes_settings import router as settings_router

# Create SQLite database tables
Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"==================================================")
    print(f" {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f" Database: {settings.DATABASE_URL}")
    print(f" Storage Directory: {settings.STORAGE_DIR}")
    print(f" AI Provider: {settings.AI_PROVIDER}")
    print(f" TTS Engine: {settings.TTS_ENGINE}")
    print(f"==================================================")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Doctor-Led Metabolic Health Research-to-Content Pipeline for Steer",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local frontend dev server on any port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    origin = request.headers.get("origin") or "*"
    headers = {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    if origin != "*":
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
        headers=headers
    )


# Include Routers
app.include_router(settings_router)
app.include_router(projects_router)
app.include_router(claims_router)
app.include_router(content_router)
app.include_router(artifacts_router)
app.include_router(export_router)

# Mount generated storage directory for direct static serving
settings.generated_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static/generated", StaticFiles(directory=str(settings.generated_dir)), name="generated")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
