from __future__ import annotations

from datetime import date, datetime
from numbers import Number
from typing import Dict, Iterable, List


COLUMN_ORDER = [
    "pri_id",
    "pri_cellular_number",
    "pri_sim_msisdn",
    "pri_sim_imsi",
    "pri_action",
    "pri_level_action",
    "pri_status",
    "pri_action_date",
    "pri_system_date",
    "pri_ne_type",
    "pri_ne_id",
    "pri_ne_service",
    "pri_source_application",
    "pri_source_app_id",
    "pri_sis_id",
    "pri_error_code",
    "pri_message_error",
    "pri_correlation_id",
    "pri_reason_code",
    "pri_processed_date",
    "pri_in_queue",
    "pri_response_date",
    "pri_delivered_safir",
    "pri_received_safir",
    "pri_id_sended",
    "pri_user_sender",
    "pri_ne_entity",
    "pri_acc_id",
    "pri_main_pri_id",
    "pri_resp_manager",
    "pri_usr_id",
    "pri_priority_usr",
    "pri_priority_date",
    "pri_save_last_tx_status",
    "pri_crm_action",
    "pri_request",
    "pri_response",
    "pri_sended_count",
    "pri_main_sis_id",
    "pri_imei",
    "pri_card_number",
    "pri_correlator_id",
]

SQL_DATE_FORMAT = "YYYY-MM-DD HH24:MI:SS"


def _escape_string(value: str) -> str:
    return value.replace("'", "''")


def _format_datetime(value: datetime) -> str:
    formatted = value.strftime("%Y-%m-%d %H:%M:%S")
    return f"TO_DATE('{formatted}','{SQL_DATE_FORMAT}')"


def _looks_like_datetime_string(value: str) -> bool:
    return len(value) >= 16 and "-" in value and ":" in value


def esc(value) -> str:  # noqa: ANN001 - especificación externa
    if value is None:
        return "NULL"

    if isinstance(value, (datetime, date)):
        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())
        return _format_datetime(value)

    if isinstance(value, Number) and not isinstance(value, bool):
        return str(value)

    text = str(value)
    if _looks_like_datetime_string(text):
        return f"TO_DATE('{text}','{SQL_DATE_FORMAT}')"

    return f"'{_escape_string(text)}'"


def generate_insert_statements(rows: Iterable[Dict[str, object]]) -> str:
    statements: List[str] = []
    for row in rows:
        values = [esc(row.get(column)) for column in COLUMN_ORDER]
        value_clause = ", ".join(values)
        statement = (
            "INSERT INTO swp_provisioning_interfaces ("
            + ", ".join(COLUMN_ORDER)
            + f") VALUES ({value_clause});"
        )
        statements.append(statement)
    return "\n".join(statements)
