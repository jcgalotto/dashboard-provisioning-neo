from provisioning_api.db.oracle import fetch_all, fetch_count
from provisioning_api.db.sql.queries import build_sql

def _supports_offset_fetch(con) -> bool:
    try:
        major = int(con.version.split(".")[0])
        return major >= 12
    except Exception:
        return True  # si no sabemos, asumimos 12+

def fetch_records(con, filters: dict, paginated: bool = True):
    legacy = not _supports_offset_fetch(con)
    select_sql, count_sql, binds = build_sql(
        filters, include_pagination=paginated, use_legacy_pagination=legacy
    )

    items = fetch_all(con, select_sql, binds)

    if paginated:
        binds_count = {k: v for k, v in binds.items() if k not in ("offset", "limit")}
        total = fetch_count(con, count_sql, binds_count) if count_sql else len(items)
    else:
        total = fetch_count(con, count_sql, binds) if count_sql else len(items)
    return items, int(total)
