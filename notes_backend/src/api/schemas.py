"""Pydantic schemas for the Notes API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base fields shared by note input models."""

    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=0, description="Note content/body")


class NoteCreate(NoteBase):
    """Payload to create a note."""
    pass


class NoteUpdate(BaseModel):
    """Payload to update a note (partial updates supported)."""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated title")
    content: Optional[str] = Field(None, min_length=0, description="Updated content/body")


class NoteRead(NoteBase):
    """Note representation returned by the API."""

    id: int = Field(..., description="Note ID")
    created_at: str = Field(..., description="ISO-8601 UTC timestamp when the note was created")
    updated_at: str = Field(..., description="ISO-8601 UTC timestamp when the note was last updated")


class NotesList(BaseModel):
    """List response for notes."""

    items: list[NoteRead] = Field(..., description="List of notes")
