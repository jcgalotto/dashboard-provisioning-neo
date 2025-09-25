from contextlib import contextmanager
from typing import Iterator

import oracledb

from models import DbCredentials


oracledb.defaults.fetch_lobs = False


@contextmanager
def oracle_connection(credentials: DbCredentials) -> Iterator[oracledb.Connection]:
    dsn = f"{credentials.host}:{credentials.port}/{credentials.service}"
    connection = oracledb.connect(
        user=credentials.user,
        password=credentials.password,
        dsn=dsn,
    )
    try:
        yield connection
    finally:
        connection.close()
