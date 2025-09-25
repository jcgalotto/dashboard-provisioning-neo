from __future__ import annotations

from typing import Dict, List, Tuple

from models import FilterParams


SELECT_COLUMNS = """
  a.pri_id,
  a.pri_cellular_number,
  a.pri_sim_msisdn,
  a.pri_sim_imsi,
  a.pri_action,
  a.pri_level_action,
  a.pri_status,
  TO_CHAR(a.pri_action_date, 'YYYY-MM-DD HH24:MI:SS') AS pri_action_date,
  TO_CHAR(a.pri_system_date, 'YYYY-MM-DD HH24:MI:SS') AS pri_system_date,
  a.pri_ne_type,
  a.pri_ne_id,
  a.pri_ne_service,
  a.pri_source_application,
  a.pri_source_app_id,
  a.pri_sis_id,
  TO_CHAR(a.pri_error_code) AS pri_error_code,
  a.pri_message_error,
  a.pri_correlation_id,
  a.pri_reason_code,
  TO_CHAR(a.pri_processed_date, 'YYYY-MM-DD HH24:MI:SS') AS pri_processed_date,
  TO_CHAR(a.pri_in_queue, 'YYYY-MM-DD HH24:MI:SS') AS pri_in_queue,
  TO_CHAR(a.pri_response_date, 'YYYY-MM-DD HH24:MI:SS') AS pri_response_date,
  TO_CHAR(a.pri_delivered_safir, 'YYYY-MM-DD HH24:MI:SS') AS pri_delivered_safir,
  TO_CHAR(a.pri_received_safir, 'YYYY-MM-DD HH24:MI:SS') AS pri_received_safir,
  a.pri_id_sended,
  a.pri_user_sender,
  a.pri_ne_entity,
  a.pri_acc_id,
  a.pri_main_pri_id,
  a.pri_resp_manager,
  a.pri_usr_id,
  a.pri_priority_usr,
  TO_CHAR(a.pri_priority_date, 'YYYY-MM-DD HH24:MI:SS') AS pri_priority_date,
  a.pri_save_last_tx_status,
  a.pri_crm_action,
  a.pri_request,
  a.pri_response,
  a.pri_sended_count,
  a.pri_main_sis_id,
  a.pri_imei,
  a.pri_card_number,
  a.pri_correlator_id
"""

BASE_FROM = "FROM swp_provisioning_interfaces a"

DATE_FILTER = (
    "a.pri_action_date BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD HH24:MI:SS') "
    "AND TO_DATE(:end_date, 'YYYY-MM-DD HH24:MI:SS')"
)


def _build_filters(filters: FilterParams) -> Tuple[str, Dict[str, object]]:
    conditions = [DATE_FILTER, "a.pri_ne_id = :pri_ne_id"]
    binds: Dict[str, object] = {
        "start_date": filters.start_date,
        "end_date": filters.end_date,
        "pri_ne_id": filters.pri_ne_id,
    }

    if filters.pri_id is not None:
        conditions.append("a.pri_id = :pri_id")
        binds["pri_id"] = filters.pri_id

    if filters.pri_action is not None:
        conditions.append("a.pri_action = :pri_action")
        binds["pri_action"] = filters.pri_action

    where_clause = " WHERE " + " AND ".join(conditions)
    return where_clause, binds


def build_records_query(filters: FilterParams, include_pagination: bool = True) -> Tuple[str, Dict[str, object]]:
    where_clause, binds = _build_filters(filters)
    query = f"SELECT\n{SELECT_COLUMNS}\n{BASE_FROM}{where_clause}\nORDER BY a.pri_action_date DESC"

    if include_pagination:
        query += "\nOFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"
        binds["offset"] = filters.offset
        binds["limit"] = filters.limit

    return query, binds


def build_count_query(filters: FilterParams) -> Tuple[str, Dict[str, object]]:
    where_clause, binds = _build_filters(filters)
    query = f"SELECT COUNT(1) AS total\n{BASE_FROM}{where_clause}"
    return query, binds


def rows_to_dicts(cursor) -> List[Dict[str, object]]:
    columns = [col[0].lower() for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_query(connection, query: str, binds: Dict[str, object]) -> List[Dict[str, object]]:
    cursor = connection.cursor()
    try:
        cursor.execute(query, binds)
        return rows_to_dicts(cursor)
    finally:
        cursor.close()


def execute_count(connection, query: str, binds: Dict[str, object]) -> int:
    cursor = connection.cursor()
    try:
        cursor.execute(query, binds)
        result = cursor.fetchone()
        return int(result[0]) if result else 0
    finally:
        cursor.close()
