from __future__ import annotations

from typing import Dict, Iterable, List


DATE_COLUMNS = {
    "pri_action_date",
    "pri_system_date",
    "pri_processed_date",
    "pri_response_date",
    "pri_priority_date",
}

NUMERIC_COLUMNS = {
    "pri_id",
    "pri_id_sended",
    "pri_acc_id",
    "pri_main_pri_id",
    "pri_sended_count",
}

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


def _escape_string(value: str) -> str:
    return value.replace("'", "''")


def format_value(column: str, value) -> str:
    if value is None:
        return "NULL"

    if column in DATE_COLUMNS:
        return f"TO_DATE('{value}','YYYY-MM-DD HH24:MI:SS')"

    if isinstance(value, (int, float)) or column in NUMERIC_COLUMNS:
        return str(value)

    return f"'{_escape_string(str(value))}'"


def generate_insert_statements(rows: Iterable[Dict[str, object]]) -> str:
    statements: List[str] = []
    for row in rows:
        values = [format_value(column, row.get(column)) for column in COLUMN_ORDER]
        value_clause = ", ".join(values)
        statement = (
            "INSERT INTO swp_provisioning_interfaces (\n  "
            + ",\n  ".join(COLUMN_ORDER)
            + f"\n) VALUES ({value_clause});"
        )
        statements.append(statement)
    if not statements:
        return "\n"
    return "\n".join(statements) + "\n"
