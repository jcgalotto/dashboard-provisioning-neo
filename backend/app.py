from __future__ import annotations

import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from oracledb import DatabaseError

from db import oracle_connection
from models import RecordItem, RecordsRequest, RecordsResponse
from queries import (
    build_count_query,
    build_records_query,
    execute_count,
    execute_query,
)
from utils_sql import generate_insert_statements

logger = logging.getLogger(__name__)

app = FastAPI(title="Dashboard Provisioning NEO", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _handle_database_error(exc: DatabaseError) -> HTTPException:
    error = exc.args[0] if exc.args else exc
    message = getattr(error, "message", str(exc))
    return HTTPException(status_code=400, detail=f"Error de base de datos: {message}")


@app.post("/records", response_model=RecordsResponse)
def get_records(payload: RecordsRequest) -> RecordsResponse:
    try:
        with oracle_connection(payload.db) as connection:
            records_query, records_binds = build_records_query(payload.filters, include_pagination=True)
            items_data = list(execute_query(connection, records_query, records_binds))

            count_query, count_binds = build_count_query(payload.filters)
            total = execute_count(connection, count_query, count_binds)
    except DatabaseError as exc:  # pragma: no cover - requires DB
        logger.exception("Database error while fetching records")
        raise _handle_database_error(exc)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Unexpected error while fetching records")
        raise HTTPException(status_code=500, detail=str(exc))

    items: List[RecordItem] = [RecordItem(**row) for row in items_data]
    return RecordsResponse(items=items, count=total)


@app.post("/generate-inserts")
def generate_inserts(payload: RecordsRequest) -> Response:
    try:
        with oracle_connection(payload.db) as connection:
            records_query, records_binds = build_records_query(payload.filters, include_pagination=False)
            rows = list(execute_query(connection, records_query, records_binds))
    except DatabaseError as exc:  # pragma: no cover - requires DB
        logger.exception("Database error while generating inserts")
        raise _handle_database_error(exc)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Unexpected error while generating inserts")
        raise HTTPException(status_code=500, detail=str(exc))

    sql_content = generate_insert_statements(rows)
    headers = {"Content-Disposition": "attachment; filename=provisioning_inserts.sql"}
    return Response(content=sql_content, media_type="application/sql", headers=headers)
