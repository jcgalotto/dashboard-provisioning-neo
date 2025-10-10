from provisioning_api.db.oracle import fetch_all


def get_distinct_options(con, filters: dict) -> dict:
    base_where = [
        "a.pri_ne_id = :pri_ne_id",
        "a.pri_action_date BETWEEN TO_DATE(:start_date,'YYYY-MM-DD HH24:MI:SS') "
        "AND TO_DATE(:end_date,'YYYY-MM-DD HH24:MI:SS')",
    ]
    binds = {
        "pri_ne_id": filters["pri_ne_id"],
        "start_date": filters["start_date"],
        "end_date": filters["end_date"],
    }

    def _q(col):
        return (
            "SELECT DISTINCT {col} AS v FROM swp_provisioning_interfaces a WHERE {where} "
            "ORDER BY {col}"
        ).format(col=col, where=" AND ".join(base_where))

    actions = [r["v"] for r in fetch_all(con, _q("a.pri_action"), binds) if r["v"] is not None]
    groups = [r["v"] for r in fetch_all(con, _q("a.pri_ne_group"), binds) if r["v"] is not None]
    status = [r["v"] for r in fetch_all(con, _q("a.pri_status"), binds) if r["v"] is not None]
    return {"pri_action": actions, "pri_ne_group": groups, "pri_status": status}
