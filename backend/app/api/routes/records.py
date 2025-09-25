"""Records endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.core.logging import logger
from app.schemas.record import RecordsRequest, RecordsResponse
from app.services.records_service import get_records

router = APIRouter()


@router.post("/records", response_model=RecordsResponse)
async def read_records(payload: RecordsRequest) -> RecordsResponse:
    """Fetch provisioning records according to provided filters."""

    try:
        items, total = get_records(payload.db.model_dump(), payload.filters.model_dump())
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error retrieving records")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudieron obtener los registros",
        ) from exc

    return RecordsResponse(items=items, total=total)
