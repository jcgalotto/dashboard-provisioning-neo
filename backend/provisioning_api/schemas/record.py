from typing import Optional, Union
from pydantic import BaseModel

Num = Union[int, float, str]


class Record(BaseModel):
    pri_id: int
    pri_cellular_number: Optional[str] = None
    pri_sim_msisdn: Optional[str] = None
    pri_sim_imsi: Optional[str] = None
    pri_action: Optional[str] = None
    pri_level_action: Optional[str] = None
    pri_status: Optional[str] = None
    pri_action_date: Optional[str] = None
    pri_system_date: Optional[str] = None
    pri_ne_type: Optional[str] = None
    pri_ne_id: Optional[str] = None
    pri_ne_service: Optional[str] = None
    pri_source_application: Optional[str] = None
    pri_source_app_id: Optional[str] = None
    pri_sis_id: Optional[Num] = None
    pri_error_code: Optional[str] = None
    pri_message_error: Optional[str] = None
    pri_correlation_id: Optional[Num] = None
    pri_reason_code: Optional[str] = None
    pri_processed_date: Optional[str] = None
    pri_in_queue: Optional[str] = None
    pri_response_date: Optional[str] = None
    pri_delivered_safir: Optional[str] = None
    pri_received_safir: Optional[str] = None
    pri_id_sended: Optional[Num] = None
    pri_user_sender: Optional[str] = None
    pri_ne_entity: Optional[str] = None
    pri_acc_id: Optional[Num] = None
    pri_main_pri_id: Optional[Num] = None
    pri_resp_manager: Optional[str] = None
    pri_usr_id: Optional[Num] = None
    pri_priority_usr: Optional[str] = None
    pri_priority_date: Optional[str] = None
    pri_save_last_tx_status: Optional[str] = None
    pri_crm_action: Optional[str] = None
    pri_request: Optional[str] = None
    pri_response: Optional[str] = None
    pri_sended_count: Optional[Num] = None
    pri_main_sis_id: Optional[Num] = None
    pri_imei: Optional[str] = None
    pri_card_number: Optional[str] = None
    pri_correlator_id: Optional[Num] = None


class RecordsResponse(BaseModel):
    items: list[Record]
    total: int


class DBParams(BaseModel):
    host: str
    port: int
    service: str
    user: str
    password: str


class Filters(BaseModel):
    start_date: str
    end_date: str
    pri_ne_id: str
    pri_id: Optional[int] = None
    pri_action: Optional[str] = None
    limit: int = 200
    offset: int = 0


class RecordsRequest(BaseModel):
    db: DBParams
    filters: Filters
