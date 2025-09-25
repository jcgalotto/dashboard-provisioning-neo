from typing import Any, Iterable
from datetime import datetime, date

# Lista completa y ordenada de columnas
COLUMNS = [
  "pri_id","pri_cellular_number","pri_sim_msisdn","pri_sim_imsi","pri_action",
  "pri_level_action","pri_status","pri_action_date","pri_system_date","pri_ne_type",
  "pri_ne_id","pri_ne_service","pri_source_application","pri_source_app_id","pri_sis_id",
  "pri_error_code","pri_message_error","pri_correlation_id","pri_reason_code","pri_processed_date",
  "pri_in_queue","pri_response_date","pri_delivered_safir","pri_received_safir","pri_id_sended",
  "pri_user_sender","pri_ne_entity","pri_acc_id","pri_main_pri_id","pri_resp_manager",
  "pri_usr_id","pri_priority_usr","pri_priority_date","pri_save_last_tx_status","pri_crm_action",
  "pri_request","pri_response","pri_sended_count","pri_main_sis_id","pri_imei",
  "pri_card_number","pri_correlator_id"
]

# Expresiones RAW que deben insertarse sin escapado ni comillas
RAW = {
    "pri_id": "(SELECT NVL(MAX(pri_id), 0) + 1 FROM swp_provisioning_interfaces)",
    "pri_action_date": "TO_DATE('30-04-2025 00:00:01', 'DD-MM-YYYY HH24:MI:SS')",
    "pri_system_date": "TO_DATE('30-04-2025 00:00:01', 'DD-MM-YYYY HH24:MI:SS')",
}

INSERT_HEAD = "INSERT INTO swp_provisioning_interfaces (" + ", ".join(COLUMNS) + ") VALUES ("

def esc(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (datetime, date)):
        s = value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else value.strftime("%Y-%m-%d 00:00:00")
        return f"TO_DATE('{s}', 'YYYY-MM-DD HH24:MI:SS')"
    s = str(value)
    # Heurística para string con formato fecha
    if ("-" in s and ":" in s and len(s) >= 16):
        return f"TO_DATE('{s.replace("'","''")}', 'YYYY-MM-DD HH24:MI:SS')"
    return "'" + s.replace("'", "''") + "'"

def rows_to_insert_sql(rows: Iterable[dict]) -> str:
    lines = []
    for r in rows:
        vals = []
        for col in COLUMNS:
            if col in RAW:
                vals.append(RAW[col])  # usar expresión RAW
            else:
                vals.append(esc(r.get(col)))
        lines.append(INSERT_HEAD + ", ".join(vals) + ");")
    return "\n".join(lines) + "\n"
