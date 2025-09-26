# backend/provisioning_api/db/oracle.py
from contextlib import contextmanager
import os
import socket
import oracledb

# Traer CLOB/BLOB como str/bytes
oracledb.defaults.fetch_lobs = False

def _init_thick_if_configured():
    """Inicializa modo thick si hay Instant Client disponible."""
    if not oracledb.is_thin_mode():
        return
    lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")
    try:
        if lib_dir:
            oracledb.init_oracle_client(lib_dir=lib_dir)
        else:
            # si el instant client está en PATH, esto alcanza
            oracledb.init_oracle_client()
    except Exception:
        # si ya estaba inicializado o no hay client, dejamos que el connect falle como siempre
        pass

def _dsn_service(host: str, port: int, service: str) -> str:
    # service_name primero (lo más común)
    return oracledb.makedsn(host, port, service_name=service)

def _dsn_sid(host: str, port: int, sid: str) -> str:
    # fallback a SID cuando el listener no tiene el service_name
    return oracledb.makedsn(host, port, sid=sid)

@contextmanager
def connect(db: dict):
    host = db["host"].strip()
    port = int(db["port"])
    service = db["service"].strip()

    # 1) DNS upfront para mensaje claro
    try:
        socket.getaddrinfo(host, None)
    except socket.gaierror as e:
        raise RuntimeError(f"No se puede resolver el host '{host}' (DNS/VPN). Detalle: {e}")

    def _try_connect(dsn):
        return oracledb.connect(user=db["user"], password=db["password"], dsn=dsn)

    # 2) Intento en thin con service_name
    dsn = _dsn_service(host, port, service)
    try:
        con = _try_connect(dsn)
    except oracledb.DatabaseError as e:
        msg = str(e)
        # a) DB vieja no soporta thin -> cambiamos a thick y reintentamos
        if "DPY-3010" in msg:
            _init_thick_if_configured()
            con = _try_connect(dsn)
        # b) listener no conoce el service_name -> probamos con SID
        elif "ORA-12514" in msg or "ORA-12505" in msg:
            dsn_sid = _dsn_sid(host, port, service)
            con = _try_connect(dsn_sid)
        else:
            raise

    try:
        yield con
    finally:
        try:
            con.close()
        except Exception:
            pass

def fetch_all(con, sql: str, binds: dict) -> list[dict]:
    # arraysize ajustable si querés performance: cur.arraysize = 1000
    with con.cursor() as cur:
        cur.execute(sql, binds)
        rows = cur.fetchall()
        cols = [d[0].lower() for d in cur.description]
    return [dict(zip(cols, r)) for r in rows]
