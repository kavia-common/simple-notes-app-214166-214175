"""Repository layer for notes persistence."""
from __future__ import annotations

from typing import Optional

from src.api.db import get_connection, utc_now_iso
from src.api.schemas import NoteCreate, NoteRead, NoteUpdate


def _row_to_note(row) -> NoteRead:
    """Convert sqlite Row to NoteRead."""
    return NoteRead(
        id=int(row["id"]),
        title=str(row["title"]),
        content=str(row["content"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def list_notes() -> list[NoteRead]:
    """Return all notes ordered by updated_at desc."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC, id DESC"
        )
        rows = cur.fetchall()
        return [_row_to_note(r) for r in rows]


def get_note(note_id: int) -> Optional[NoteRead]:
    """Return a single note or None if missing."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cur.fetchone()
        return _row_to_note(row) if row else None


def create_note(payload: NoteCreate) -> NoteRead:
    """Create and return a new note."""
    now = utc_now_iso()
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (payload.title, payload.content, now, now),
        )
        conn.commit()
        note_id = int(cur.lastrowid)

    # Re-read to ensure consistent return
    created = get_note(note_id)
    assert created is not None
    return created


def update_note(note_id: int, payload: NoteUpdate) -> Optional[NoteRead]:
    """Update a note. Returns updated note, or None if missing."""
    existing = get_note(note_id)
    if existing is None:
        return None

    new_title = payload.title if payload.title is not None else existing.title
    new_content = payload.content if payload.content is not None else existing.content
    now = utc_now_iso()

    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (new_title, new_content, now, note_id),
        )
        conn.commit()

    updated = get_note(note_id)
    assert updated is not None
    return updated


def delete_note(note_id: int) -> bool:
    """Delete a note. Returns True if deleted, False if missing."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return cur.rowcount > 0
