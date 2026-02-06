"""Notes API router."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from src.api.repository import create_note, delete_note, get_note, list_notes, update_note
from src.api.schemas import NoteCreate, NoteRead, NotesList, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(
    "",
    response_model=NotesList,
    summary="List notes",
    description="Return all notes ordered by last update time (descending).",
    operation_id="list_notes",
)
def list_notes_route() -> NotesList:
    """List notes endpoint."""
    return NotesList(items=list_notes())


@router.post(
    "",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with title and content.",
    operation_id="create_note",
)
def create_note_route(payload: NoteCreate) -> NoteRead:
    """Create note endpoint."""
    return create_note(payload)


@router.get(
    "/{note_id}",
    response_model=NoteRead,
    summary="Get a note",
    description="Get a single note by ID.",
    operation_id="get_note",
)
def get_note_route(note_id: int) -> NoteRead:
    """Get note endpoint."""
    note = get_note(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put(
    "/{note_id}",
    response_model=NoteRead,
    summary="Update a note",
    description="Update an existing note by ID (partial updates supported).",
    operation_id="update_note",
)
def update_note_route(note_id: int, payload: NoteUpdate) -> NoteRead:
    """Update note endpoint."""
    updated = update_note(note_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by ID.",
    operation_id="delete_note",
)
def delete_note_route(note_id: int) -> None:
    """Delete note endpoint."""
    ok = delete_note(note_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
