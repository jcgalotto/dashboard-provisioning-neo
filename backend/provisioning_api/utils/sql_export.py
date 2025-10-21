from typing import Any, Dict, Iterable, List
import datetime as dt
import re

COLUMNS = [
  "pri_id","pri_cellular_number","pri_sim_msisdn","pri_sim_imsi","pri_action",
  "pri_level_action","pri_status","pri_action_date","pri_system_date","pri_ne_type",
  "pri_ne_id","pri_ne_service","pri_source_application","pri_source_app_id","pri_sis_id",
  "pri_error_code","pri_message_error","pri_correlation_id","pri_reason_code","pri_processed_date",
  "pri_response_date","pri_priority_date","pri_in_queue","pri_delivered_safir","pri_received_safir",
  "pri_id_sended","pri_user_sender","pri_ne_entity","pri_acc_id","pri_main_pri_id","pri_resp_manager",
  "pri_usr_id","pri_priority_usr","pri_save_last_tx_status","pri_crm_action","pri_request","pri_response",
  "pri_sended_count","pri_main_sis_id","pri_imei","pri_card_number","pri_correlator_id"
]

RAW_OVERRIDES = {
  "pri_id": "(SELECT NVL(MAX(pri_id), 0) + 1 FROM swp_provisioning_interfaces)",
  "pri_action_date": "TO_DATE('30-04-2025 00:00:01', 'DD-MM-YYYY HH24:MI:SS')",
  "pri_system_date": "TO_DATE('30-04-2025 00:00:01', 'DD-MM-YYYY HH24:MI:SS')",
  "pri_status": "PENDING"
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
NUM_RE  = re.compile(r"^-?\d+(?:\.\d+)?$")


def esc(v: Any) -> str:
    if v is None: return "NULL"
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, dt.datetime):
        s = v.strftime("%Y-%m-%d %H:%M:%S"); return f"TO_DATE('{s}','YYYY-MM-DD HH24:MI:SS')"
    if isinstance(v, dt.date):
        s = v.strftime("%Y-%m-%d 00:00:00"); return f"TO_DATE('{s}','YYYY-MM-DD HH24:MI:SS')"
    s = str(v).strip()
    if DATE_RE.match(s): return f"TO_DATE('{s}','YYYY-MM-DD HH24:MI:SS')"
    if NUM_RE.match(s):  return s
    s_esc = s.replace("'", "''")
    return f"'{s_esc}'"


def _format_row(row: Dict[str, Any]) -> List[str]:
    out: List[str] = []
    for col in COLUMNS:
        if col in RAW_OVERRIDES:
            out.append(RAW_OVERRIDES[col])
        else:
            out.append(esc(row.get(col)))
    return out


def generate_insert_statements(rows: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = []
    cols = ", ".join(COLUMNS)
    for r in rows:
        values = ", ".join(_format_row(r))
        lines.append(f"INSERT INTO swp_provisioning_interfaces ({cols}) VALUES ({values});")
    return "\n".join(lines) + "\n"
