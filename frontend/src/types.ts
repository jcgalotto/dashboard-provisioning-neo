export interface DbCredentials {
  host: string;
  port: number;
  service: string;
  user: string;
  password: string;
}

export interface Filters {
  start_date: string;
  end_date: string;
  pri_ne_id: string;
  pri_id?: string;
  pri_action?: string;
}

export interface RecordItem {
  pri_id: number | null;
  pri_cellular_number: string | null;
  pri_sim_msisdn: string | null;
  pri_sim_imsi: string | null;
  pri_action: string | null;
  pri_level_action: string | null;
  pri_status: string | null;
  pri_action_date: string | null;
  pri_system_date: string | null;
  pri_ne_type: string | null;
  pri_ne_id: string | null;
  pri_ne_service: string | null;
  pri_source_application: string | null;
  pri_source_app_id: string | null;
  pri_sis_id: string | null;
  pri_error_code: string | null;
  pri_message_error: string | null;
  pri_correlation_id: string | null;
  pri_reason_code: string | null;
  pri_processed_date: string | null;
  pri_in_queue: string | null;
  pri_response_date: string | null;
  pri_delivered_safir: string | null;
  pri_received_safir: string | null;
  pri_id_sended: number | null;
  pri_user_sender: string | null;
  pri_ne_entity: string | null;
  pri_acc_id: number | null;
  pri_main_pri_id: number | null;
  pri_resp_manager: string | null;
  pri_usr_id: string | null;
  pri_priority_usr: string | null;
  pri_priority_date: string | null;
  pri_save_last_tx_status: string | null;
  pri_crm_action: string | null;
  pri_request: string | null;
  pri_response: string | null;
  pri_sended_count: number | null;
  pri_main_sis_id: string | null;
  pri_imei: string | null;
  pri_card_number: string | null;
  pri_correlator_id: string | null;
}

export interface RecordsResponse {
  items: RecordItem[];
  count: number;
}

export interface ApiPayload {
  db: DbCredentials;
  filters: {
    start_date: string;
    end_date: string;
    pri_ne_id: string;
    pri_id?: number;
    pri_action?: string;
    limit: number;
    offset: number;
  };
}
