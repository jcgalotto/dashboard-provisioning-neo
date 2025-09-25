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

export type Maybe<T> = T | null;

export type FlexibleNumeric = number | string;

export interface RecordItem {
  pri_id: FlexibleNumeric;
  pri_cellular_number: Maybe<string>;
  pri_sim_msisdn: Maybe<string>;
  pri_sim_imsi: Maybe<string>;
  pri_action: Maybe<string>;
  pri_level_action: Maybe<string>;
  pri_status: Maybe<string>;
  pri_action_date: Maybe<string>;
  pri_system_date: Maybe<string>;
  pri_ne_type: Maybe<string>;
  pri_ne_id: Maybe<string>;
  pri_ne_service: Maybe<string>;
  pri_source_application: Maybe<string>;
  pri_source_app_id: Maybe<string>;
  pri_sis_id: Maybe<FlexibleNumeric>;
  pri_error_code: Maybe<string>;
  pri_message_error: Maybe<string>;
  pri_correlation_id: Maybe<FlexibleNumeric>;
  pri_reason_code: Maybe<string>;
  pri_processed_date: Maybe<string>;
  pri_in_queue: Maybe<string>;
  pri_response_date: Maybe<string>;
  pri_delivered_safir: Maybe<string>;
  pri_received_safir: Maybe<string>;
  pri_id_sended: Maybe<FlexibleNumeric>;
  pri_user_sender: Maybe<string>;
  pri_ne_entity: Maybe<string>;
  pri_acc_id: Maybe<FlexibleNumeric>;
  pri_main_pri_id: Maybe<FlexibleNumeric>;
  pri_resp_manager: Maybe<string>;
  pri_usr_id: Maybe<FlexibleNumeric>;
  pri_priority_usr: Maybe<string>;
  pri_priority_date: Maybe<string>;
  pri_save_last_tx_status: Maybe<string>;
  pri_crm_action: Maybe<string>;
  pri_request: Maybe<string>;
  pri_response: Maybe<string>;
  pri_sended_count: Maybe<FlexibleNumeric>;
  pri_main_sis_id: Maybe<FlexibleNumeric>;
  pri_imei: Maybe<string>;
  pri_card_number: Maybe<string>;
  pri_correlator_id: Maybe<FlexibleNumeric>;
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
    pri_id?: number;
    pri_action?: string;
    limit: number;
    offset: number;
  };
}
