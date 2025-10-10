from provisioning_api.db.oracle import fetch_all


def get_distinct_options(con, f: dict) -> dict:
    where = [
        "a.pri_ne_id = :pri_ne_id",
        "a.pri_action_date BETWEEN TO_DATE(:start_date,'YYYY-MM-DD HH24:MI:SS') AND TO_DATE(:end_date,'YYYY-MM-DD HH24:MI:SS')",
    ]
    binds = {
        "pri_ne_id": f["pri_ne_id"],
        "start_date": f["start_date"],
        "end_date": f["end_date"],
    }

    def q(col: str) -> str:
        return f"SELECT DISTINCT {col} AS v FROM swp_provisioning_interfaces a WHERE {' AND '.join(where)} ORDER BY {col}"

    actions = [r["v"] for r in fetch_all(con, q("a.pri_action"), binds) if r["v"] is not None]
    groups = [r["v"] for r in fetch_all(con, q("a.pri_ne_group"), binds) if r["v"] is not None]
    status = [r["v"] for r in fetch_all(con, q("a.pri_status"), binds) if r["v"] is not None]
    return {"pri_action": actions, "pri_ne_group": groups, "pri_status": status}
