from contextlib import contextmanager
import os
import oracledb

oracledb.defaults.fetch_lobs = False

_THICK_READY = False
_THICK_ERR = None


def _maybe_init_thick_on_import():
    """
    Decide driver mode BEFORE any connection is attempted.
    If FORCE_ORACLE_THICK=1 or ORACLE_CLIENT_LIB_DIR is set -> try THICK now.
    Never attempt switching later (prevents DPY-2019).
    """
    global _THICK_READY, _THICK_ERR
    force = os.getenv("FORCE_ORACLE_THICK") == "1"
    lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")

    if not (force or lib_dir):
        # stay in THIN, do nothing
        return

    try:
        if lib_dir:
            oracledb.init_oracle_client(lib_dir=lib_dir)
        else:
            # rely on PATH having the Instant Client directory
            oracledb.init_oracle_client()
        _THICK_READY = True
    except Exception as e:
        _THICK_ERR = e
        _THICK_READY = False


# initialize mode at import time
_maybe_init_thick_on_import()


def _dsn_from(db: dict) -> str:
    """
    Support service or SID:
      - service: host:port/service
      - sid    : host:port:SID   (if user typed something containing ':')
    We'll accept whatever the UI passes in 'service' and not second-guess it.
    """
    svc = (db.get("service") or "").strip()
    return f'{db["host"]}:{db["port"]}/{svc}'.rstrip("/")


@contextmanager
def connect(db: dict):
    """
    Deterministic mode:
      - If THICK was initialized at import, we are in THICK.
      - Else THIN is used; if server is too old (DPY-3010), raise a clear error
        instructing to start the process with THICK pre-initialized.
    """
    dsn = _dsn_from(db)

    # If THICK was requested but failed to init at import, fail fast with guidance
    if os.getenv("FORCE_ORACLE_THICK") == "1" and not _THICK_READY:
        raise RuntimeError(
            "El servidor requiere modo THICK pero no está disponible. "
            "No se pudo iniciar Oracle Instant Client. "
            "Configurá ORACLE_CLIENT_LIB_DIR o agregá la carpeta al PATH. "
            f"Detalle: {repr(_THICK_ERR)}"
        )

    try:
        con = oracledb.connect(user=db["user"], password=db["password"], dsn=dsn)
    except oracledb.DatabaseError as err:
        msg = str(err)
        if "DPY-3010" in msg:
            # Too old for THIN. We cannot switch now (DPY-2019), so instruct restart.
            hint = []
            if not _THICK_READY:
                hint.append(
                    "Este servidor Oracle no es soportado en modo THIN. "
                    "Iniciá la app con THICK pre-inicializado: "
                    "instalá Instant Client 19/21 y seteá ORACLE_CLIENT_LIB_DIR "
                    "o agregá su carpeta al PATH, luego reiniciá el servicio/proceso."
                )
            raise RuntimeError("Conexión rechazada (DPY-3010). " + " ".join(hint))
        raise RuntimeError(
            f"Conexión Oracle fallida: {err}. "
            "Verificá host/puerto/servicio y reachability (firewall/VPN)."
        )

    try:
        yield con
    finally:
        try:
            con.close()
        except Exception:
            pass


def fetch_all(con, sql: str, binds: dict) -> list[dict]:
    cur = con.cursor()
    cur.execute(sql, binds)
    rows = cur.fetchall()
    cols = [d[0].lower() for d in cur.description]
    return [dict(zip(cols, r)) for r in rows]


def fetch_one(con, sql: str, binds: dict):
    cur = con.cursor()
    cur.execute(sql, binds)
    return cur.fetchone()


def fetch_count(con, sql: str, binds: dict) -> int:
    cur = con.cursor()
    cur.execute(sql, binds)
    row = cur.fetchone()
    return int(row[0]) if row and row[0] is not None else 0
