"""Business logic for provisioning records."""
from __future__ import annotations

from typing import Any, Dict, Tuple

from ..provisioning_api.db.oracle import connect
from ..provisioning_api.repositories.records_repository import fetch_all_records, fetch_records
from ..provisioning_api.utils.sql_export import generate_insert_statements


def get_records(db: Dict[str, Any], filters: Dict[str, Any]) -> Tuple[list[Dict[str, Any]], int]:
    """Retrieve records by delegating to the repository with managed connection."""

    with connect(db) as connection:
        return fetch_records(connection, filters)


def generate_inserts(db: Dict[str, Any], filters: Dict[str, Any]) -> str:
    """Generate INSERT statements for all records that match the filters."""

    export_filters = dict(filters)
    export_filters.pop("limit", None)
    export_filters.pop("offset", None)

    with connect(db) as connection:
        rows = fetch_all_records(connection, export_filters)
    return generate_insert_statements(rows)
