from provisioning_api.db.oracle import fetch_all
from provisioning_api.db.sql.queries import build_sql

def fetch_records(con, filters: dict, paginated: bool = True):
    sql, count_sql, binds = build_sql(filters, include_pagination=paginated)
    items = fetch_all(con, sql, binds)
    total = fetch_all(con, count_sql, binds)[0]["total"] if paginated else len(items)
    return items, int(total)
