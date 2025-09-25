"""AI assisted endpoints."""
from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from app.ai.graph import run_pipeline
from app.core.logging import logger

router = APIRouter()


class AIRequest(BaseModel):
    text: str


@router.post("/ai/ask")
async def ask_ai(payload: AIRequest):
    """Process natural language query to derive filters and SQL."""

    try:
        result = run_pipeline(payload.text)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error ejecutando pipeline de IA")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo interpretar la consulta",
        ) from exc

    return result
