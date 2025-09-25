"""Oracle database utilities."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, Iterable, Iterator, List, Optional

import oracledb

oracledb.defaults.fetch_lobs = False


@contextmanager
def connect(db: Dict[str, Any]) -> Iterator[oracledb.Connection]:
    """Yield a thin connection to Oracle using provided credentials."""

    dsn = f"{db['host']}:{db['port']}/{db['service']}"
    connection = oracledb.connect(
        user=db["user"], password=db["password"], dsn=dsn
    )
    try:
        yield connection
    finally:
        connection.close()


def _rows_to_dicts(cursor: oracledb.Cursor, rows: Iterable[Iterable[Any]]) -> List[Dict[str, Any]]:
    columns = [col[0].lower() for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def fetch_all(
    connection: oracledb.Connection, sql: str, binds: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Execute a query and return all rows as dictionaries."""

    cursor = connection.cursor()
    try:
        cursor.execute(sql, binds or {})
        rows = cursor.fetchall()
        return _rows_to_dicts(cursor, rows)
    finally:
        cursor.close()


def fetch_one(
    connection: oracledb.Connection, sql: str, binds: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Execute a query and return the first row as a dictionary."""

    cursor = connection.cursor()
    try:
        cursor.execute(sql, binds or {})
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [col[0].lower() for col in cursor.description]
        return dict(zip(columns, row))
    finally:
        cursor.close()
