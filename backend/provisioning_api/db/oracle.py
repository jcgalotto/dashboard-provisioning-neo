from contextlib import contextmanager
import oracledb

# traer CLOB/BLOB como str/bytes
oracledb.defaults.fetch_lobs = False


@contextmanager
def connect(db: dict):
    dsn = f'{db["host"]}:{db["port"]}/{db["service"]}'
    con = oracledb.connect(user=db["user"], password=db["password"], dsn=dsn)
    try:
        yield con
    finally:
        con.close()


def fetch_all(con, sql: str, binds: dict) -> list[dict]:
    cur = con.cursor()
    cur.execute(sql, binds)
    rows = cur.fetchall()
    cols = [d[0].lower() for d in cur.description]
    return [dict(zip(cols, r)) for r in rows]
