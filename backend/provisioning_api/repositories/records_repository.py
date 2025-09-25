from provisioning_api.db.oracle import fetch_all
from provisioning_api.db.sql.queries import build_sql

def fetch_records(con, filters: dict, paginated: bool = True):
    select_sql, count_sql, binds = build_sql(filters, include_pagination=paginated)

    # Items con todos los binds
    items = fetch_all(con, select_sql, binds)

    # Count sin offset/limit
    if paginated:
        binds_count = {k: v for k, v in binds.items() if k not in ("offset", "limit")}
    else:
        binds_count = binds

    total = fetch_all(con, count_sql, binds_count)[0]["total"] if count_sql else len(items)
    return items, int(total)
