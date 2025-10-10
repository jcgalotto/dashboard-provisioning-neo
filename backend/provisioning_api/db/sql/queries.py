def _is_set(val):
    if val is None:
        return False
    text = str(val).strip()
    if text == "":
        return False
    return text.upper() != "TODOS"


def build_sql(filters: dict, include_pagination: bool, use_legacy_pagination: bool = False):
    where = [
        "a.pri_action_date BETWEEN TO_DATE(:start_date,'YYYY-MM-DD HH24:MI:SS') "
        "AND TO_DATE(:end_date,'YYYY-MM-DD HH24:MI:SS')",
        "a.pri_ne_id = :pri_ne_id",
    ]
    binds = {
        "start_date": filters["start_date"],
        "end_date": filters["end_date"],
        "pri_ne_id": filters["pri_ne_id"],
    }
    if _is_set(filters.get("pri_id")):
        where.append("a.pri_id = :pri_id")
        binds["pri_id"] = filters.get("pri_id")
    if _is_set(filters.get("pri_action")):
        where.append("a.pri_action = :pri_action")
        binds["pri_action"] = filters.get("pri_action")
    if _is_set(filters.get("pri_ne_group")):
        where.append("a.pri_ne_group = :pri_ne_group")
        binds["pri_ne_group"] = filters.get("pri_ne_group")
    if _is_set(filters.get("pri_status")):
        where.append("a.pri_status = :pri_status")
        binds["pri_status"] = filters.get("pri_status")

    where_clause = " AND ".join(where)
    select_columns = [
        "a.pri_id",
        "a.pri_cellular_number",
        "a.pri_sim_msisdn",
        "a.pri_sim_imsi",
        "a.pri_action",
        "a.pri_level_action",
        "a.pri_status",
        "TO_CHAR(a.pri_action_date,'YYYY-MM-DD HH24:MI:SS') AS pri_action_date",
        "TO_CHAR(a.pri_system_date,'YYYY-MM-DD HH24:MI:SS') AS pri_system_date",
        "a.pri_ne_type",
        "a.pri_ne_id",
        "a.pri_ne_service",
        "a.pri_source_application",
        "a.pri_source_app_id",
        "a.pri_sis_id",
        "TO_CHAR(a.pri_error_code) AS pri_error_code",
        "a.pri_message_error",
        "a.pri_correlation_id",
        "a.pri_reason_code",
        "TO_CHAR(a.pri_processed_date,'YYYY-MM-DD HH24:MI:SS') AS pri_processed_date",
        "TO_CHAR(a.pri_response_date,'YYYY-MM-DD HH24:MI:SS') AS pri_response_date",
        "TO_CHAR(a.pri_priority_date,'YYYY-MM-DD HH24:MI:SS') AS pri_priority_date",
        "TO_CHAR(a.pri_in_queue,'YYYY-MM-DD HH24:MI:SS') AS pri_in_queue",
        "TO_CHAR(a.pri_delivered_safir,'YYYY-MM-DD HH24:MI:SS') AS pri_delivered_safir",
        "TO_CHAR(a.pri_received_safir,'YYYY-MM-DD HH24:MI:SS') AS pri_received_safir",
        "a.pri_id_sended",
        "a.pri_user_sender",
        "a.pri_ne_entity",
        "a.pri_acc_id",
        "a.pri_main_pri_id",
        "a.pri_resp_manager",
        "a.pri_usr_id",
        "a.pri_priority_usr",
        "a.pri_save_last_tx_status",
        "a.pri_crm_action",
        "a.pri_request",
        "a.pri_response",
        "a.pri_sended_count",
        "a.pri_main_sis_id",
        "a.pri_imei",
        "a.pri_card_number",
        "a.pri_correlator_id",
    ]
    select_columns_sql = ",\n      ".join(select_columns)
    select_columns_with_rn_sql = ",\n          ".join(
        select_columns + ["ROW_NUMBER() OVER (ORDER BY a.pri_action_date DESC) AS rn"]
    )
    base_select = f"""
    SELECT
      {select_columns_sql}
    FROM swp_provisioning_interfaces a
    WHERE {where_clause}
    """

    if include_pagination:
        binds["offset"] = int(filters.get("offset", 0))
        binds["limit"] = int(filters.get("limit", 200))

        if use_legacy_pagination:
            select_sql = f"""
      SELECT q.* FROM (
        SELECT
          {select_columns_with_rn_sql}
        FROM swp_provisioning_interfaces a
        WHERE {where_clause}
      ) q
      WHERE q.rn > :offset AND q.rn <= (:offset + :limit)
      ORDER BY q.rn
    """
        else:
            select_sql = f"""
      {base_select}
      ORDER BY a.pri_action_date DESC
      OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """
    else:
        select_sql = base_select + " ORDER BY a.pri_action_date DESC"

    count_sql = f"SELECT COUNT(1) AS total FROM swp_provisioning_interfaces a WHERE {where_clause}"
    return select_sql, count_sql, binds
