"""Repository layer responsible for Oracle interactions."""
from __future__ import annotations

from typing import Any, Dict, Tuple

from app.db.oracle import fetch_all, fetch_one
from app.db.sql.queries import build_sql


def fetch_records(connection, filters: Dict[str, Any]) -> Tuple[list[Dict[str, Any]], int]:
    """Retrieve records and total count applying provided filters."""

    select_sql, select_binds, count_sql, count_binds = build_sql(filters, include_pagination=True)
    items = fetch_all(connection, select_sql, select_binds)
    count_row = fetch_one(connection, count_sql, count_binds) or {"total": 0}
    total = int(count_row.get("total", 0))
    return items, total


def fetch_all_records(connection, filters: Dict[str, Any]) -> list[Dict[str, Any]]:
    """Retrieve all records without pagination for export purposes."""

    select_sql, select_binds, _, _ = build_sql(filters, include_pagination=False)
    return fetch_all(connection, select_sql, select_binds)
