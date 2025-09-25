"""Export endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from app.core.logging import logger
from app.schemas.record import RecordsRequest
from app.services.records_service import generate_inserts

router = APIRouter()


@router.post("/generate-inserts")
async def create_inserts(payload: RecordsRequest) -> Response:
    """Generate INSERT statements for matching records."""

    try:
        sql = generate_inserts(payload.db.model_dump(), payload.filters.model_dump())
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error generating inserts")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudieron generar los INSERTs",
        ) from exc

    return Response(
        content=sql,
        media_type="application/sql",
        headers={"Content-Disposition": "attachment; filename=provisioning_inserts.sql"},
    )
