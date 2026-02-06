"""FastAPI application entrypoint for the notes backend.

Runs on the configured preview port (3001) and serves a REST API used by the React
frontend (port 3000).

Environment variables:
- SQLITE_DB: path to the sqlite database file (provided by the separate database container)
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.db import ensure_db_ready
from src.api.routers.notes import router as notes_router

openapi_tags = [
    {"name": "health", "description": "Service health and diagnostics."},
    {"name": "notes", "description": "CRUD operations for notes."},
]

app = FastAPI(
    title="Simple Notes API",
    description="REST API for creating, listing, retrieving, updating, and deleting notes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Allow the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize DB schema on startup."""
    ensure_db_ready()


@app.get(
    "/",
    tags=["health"],
    summary="Health check",
    description="Basic health check endpoint.",
    operation_id="health_check",
)
def health_check() -> dict:
    """Return service health information."""
    return {"message": "Healthy"}


app.include_router(notes_router)
