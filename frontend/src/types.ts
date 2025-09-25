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
  limit: number;
  offset: number;
}

export type FlexibleNumber = number | string;
export type Nullable<T> = T | null | undefined;

export interface RecordItem {
  pri_id: Nullable<FlexibleNumber>;
  pri_cellular_number: Nullable<string>;
  pri_sim_msisdn: Nullable<string>;
  pri_sim_imsi: Nullable<string>;
  pri_action: Nullable<string>;
  pri_level_action: Nullable<string>;
  pri_status: Nullable<string>;
  pri_action_date: Nullable<string>;
  pri_system_date: Nullable<string>;
  pri_ne_type: Nullable<string>;
  pri_ne_id: Nullable<string>;
  pri_ne_service: Nullable<string>;
  pri_source_application: Nullable<string>;
  pri_source_app_id: Nullable<FlexibleNumber>;
  pri_sis_id: Nullable<FlexibleNumber>;
  pri_error_code: Nullable<string>;
  pri_message_error: Nullable<string>;
  pri_correlation_id: Nullable<FlexibleNumber>;
  pri_reason_code: Nullable<string>;
  pri_processed_date: Nullable<string>;
  pri_response_date: Nullable<string>;
  pri_priority_date: Nullable<string>;
  pri_in_queue: Nullable<string>;
  pri_delivered_safir: Nullable<string>;
  pri_received_safir: Nullable<string>;
  pri_id_sended: Nullable<FlexibleNumber>;
  pri_user_sender: Nullable<string>;
  pri_ne_entity: Nullable<string>;
  pri_acc_id: Nullable<FlexibleNumber>;
  pri_main_pri_id: Nullable<FlexibleNumber>;
  pri_resp_manager: Nullable<string>;
  pri_usr_id: Nullable<FlexibleNumber>;
  pri_priority_usr: Nullable<string>;
  pri_save_last_tx_status: Nullable<string>;
  pri_crm_action: Nullable<string>;
  pri_request: Nullable<string>;
  pri_response: Nullable<string>;
  pri_sended_count: Nullable<FlexibleNumber>;
  pri_main_sis_id: Nullable<FlexibleNumber>;
  pri_imei: Nullable<string>;
  pri_card_number: Nullable<string>;
  pri_correlator_id: Nullable<FlexibleNumber>;
}

export interface RecordsResponse {
  items: RecordItem[];
  total: number;
}

export interface ApiPayload {
  db: DbCredentials;
  filters: {
    start_date: string;
    end_date: string;
    pri_ne_id: string;
    pri_id?: FlexibleNumber;
    pri_action?: string;
    limit: number;
    offset: number;
  };
}

export interface AskAiResponse {
  filters: Partial<{
    start_date: string;
    end_date: string;
    pri_ne_id: string;
    pri_id: FlexibleNumber;
    pri_action: string;
    limit: number;
    offset: number;
  }>;
  sql: string | null;
  errors: string[];
}
