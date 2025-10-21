"""Utilidades de conexión a Oracle con fallback automático a modo THICK."""
from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
import os
import socket
from typing import Any

import oracledb

# Traer CLOB/BLOB como str/bytes
oracledb.defaults.fetch_lobs = False

_NETWORK_HINT = (
    "No se puede conectar al listener {host}:{port}. "
    "Verificá VPN/firewall y que el listener esté activo. Detalle: {detail}"
)


def _to_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _should_force_thick() -> bool:
    return _to_bool(os.getenv("FORCE_ORACLE_THICK"))


@lru_cache(maxsize=1)
def _ensure_thick_mode() -> None:
    """Inicializa el cliente en modo THICK si es necesario."""
    if not oracledb.is_thin_mode():
        # Ya estamos en modo THICK.
        return

    lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")
    kwargs: dict[str, Any] = {}
    if lib_dir:
        kwargs["lib_dir"] = lib_dir

    try:
        oracledb.init_oracle_client(**kwargs)
    except Exception as exc:  # pragma: no cover - depende de la instalación local
        raise RuntimeError(
            "No se pudo iniciar Oracle Instant Client. "
            "Instalá Instant Client 19 u 21 y configurá ORACLE_CLIENT_LIB_DIR "
            "o agregalo al PATH. Detalle: {0}".format(exc)
        ) from exc


def _require_thick_mode(reason: str) -> None:
    try:
        _ensure_thick_mode()
    except RuntimeError as exc:
        raise RuntimeError(
            "El servidor requiere modo THICK pero no está disponible. "
            f"Motivo: {reason}. {exc}"
        ) from exc


def _parse_connection_fields(db: dict[str, Any]) -> tuple[str, int, str | None, str | None]:
    host = db["host"].strip()
    port = int(db["port"])
    raw_service = db["service"].strip()

    # Permitir host:port:SID en el campo Service
    sid = None
    service_name: str | None = raw_service or None
    if raw_service.count(":") >= 2:
        maybe_host, maybe_port, maybe_sid = raw_service.split(":", 2)
        if maybe_host and maybe_port.isdigit() and maybe_sid:
            host = maybe_host.strip()
            port = int(maybe_port)
            sid = maybe_sid.strip()
            service_name = None

    return host, port, service_name, sid


def _resolve_dns(host: str) -> None:
    try:
        socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise RuntimeError(
            f"No se puede resolver el host '{host}' (DNS/VPN). Detalle: {exc}"
        ) from exc


def _build_dsn(host: str, port: int, *, service_name: str | None = None, sid: str | None = None) -> str:
    if service_name:
        return oracledb.makedsn(host, port, service_name=service_name)
    if sid:
        return oracledb.makedsn(host, port, sid=sid)
    raise ValueError("Se requiere service_name o sid para construir el DSN")


def _is_thin_not_supported(error: Exception) -> bool:
    return "DPY-3010" in str(error)


def _is_service_not_registered(error: Exception) -> bool:
    message = str(error)
    return "ORA-12514" in message or "ORA-12505" in message


def _is_network_issue(error: Exception) -> bool:
    message = str(error)
    tokens = [
        "ORA-12170",  # timeout
        "ORA-12541",  # no listener
        "ORA-12543",  # target host or object does not exist
        "ORA-12545",  # host or object not known
        "TNS:no listener",
        "DPI-1060",
        "DPI-1072",
        "DPY-6006",
        "DPY-6005",
        "DPY-6011",
    ]
    return any(token in message for token in tokens)


def _connect_direct(db: dict[str, Any], dsn: str) -> oracledb.Connection:
    return oracledb.connect(
        user=db["user"],
        password=db["password"],
        dsn=dsn,
    )


def _with_thick_retry(db: dict[str, Any], dsn: str) -> oracledb.Connection:
    try:
        return _connect_direct(db, dsn)
    except oracledb.DatabaseError as exc:
        if _is_thin_not_supported(exc):
            _require_thick_mode("el servidor Oracle remoto no soporta modo thin (DPY-3010)")
            return _connect_direct(db, dsn)
        raise


def _handle_connection_error(error: Exception, host: str, port: int) -> None:
    if _is_network_issue(error):
        raise RuntimeError(_NETWORK_HINT.format(host=host, port=port, detail=error)) from error
    raise error


@contextmanager
def connect(db: dict[str, Any]):
    host, port, service_name, sid = _parse_connection_fields(db)
    _resolve_dns(host)

    if _should_force_thick():
        _require_thick_mode("FORCE_ORACLE_THICK=1")

    service_input = db["service"].strip()
    service_dsn = _build_dsn(host, port, service_name=service_name) if service_name else None
    sid_dsn = _build_dsn(host, port, sid=sid) if sid else None

    connection = None
    last_error: Exception | None = None

    try:
        if service_dsn:
            try:
                connection = _with_thick_retry(db, service_dsn)
            except Exception as exc:  # pragma: no cover - flujo de error
                last_error = exc
                if _is_service_not_registered(exc):
                    fallback_sid_dsn = sid_dsn
                    if fallback_sid_dsn is None and service_input:
                        fallback_sid_dsn = _build_dsn(host, port, sid=service_input)

                    if fallback_sid_dsn:
                        last_error = None
                        sid_dsn = fallback_sid_dsn
                    else:
                        _handle_connection_error(exc, host, port)
                        raise
                else:
                    _handle_connection_error(exc, host, port)
                    raise

        if connection is None and sid_dsn:
            try:
                connection = _with_thick_retry(db, sid_dsn)
            except Exception as exc:  # pragma: no cover - flujo de error
                last_error = exc
                _handle_connection_error(exc, host, port)
                raise

        if connection is None:
            # Si todo falló y no tenemos errores específicos, levantamos el último.
            if last_error:
                raise last_error
            raise RuntimeError("No se pudo establecer conexión con Oracle: parámetros incompletos")

        yield connection
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass


def fetch_all(con: oracledb.Connection, sql: str, binds: dict) -> list[dict]:
    with con.cursor() as cur:
        cur.execute(sql, binds)
        rows = cur.fetchall()
        cols = [d[0].lower() for d in cur.description]
    return [dict(zip(cols, row)) for row in rows]


def fetch_count(con: oracledb.Connection, sql: str, binds: dict) -> int:
    with con.cursor() as cur:
        cur.execute(sql, binds)
        row = cur.fetchone()
    return int(row[0] if row else 0)
