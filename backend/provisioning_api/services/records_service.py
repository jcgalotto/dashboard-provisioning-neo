from provisioning_api.db.oracle import connect
from provisioning_api.repositories.records_repository import fetch_records
from provisioning_api.utils.sql_export import generate_insert_statements

def get_records(db: dict, filters: dict):
    with connect(db) as con:
        return fetch_records(con, filters, paginated=True)

def generate_inserts(db: dict, filters: dict) -> str:
    # sin paginar para exportar todo
    with connect(db) as con:
        items, _ = fetch_records(con, filters, paginated=False)
        return generate_insert_statements(items)
