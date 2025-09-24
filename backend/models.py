from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DbCredentials(BaseModel):
    host: str
    port: int = Field(..., gt=0)
    service: str
    user: str
    password: str


class FilterParams(BaseModel):
    start_date: str
    end_date: str
    pri_ne_id: str
    pri_id: Optional[int] = None
    pri_action: Optional[str] = None
    limit: int = Field(200, gt=0)
    offset: int = Field(0, ge=0)

    @validator("start_date", "end_date")
    def validate_datetime_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, DATETIME_FORMAT)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(
                "El formato de fecha debe ser YYYY-MM-DD HH:MM:SS"
            ) from exc
        return value

    @validator("pri_action")
    def strip_empty_action(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        return value or None


class RecordsRequest(BaseModel):
    db: DbCredentials
    filters: FilterParams


class RecordItem(BaseModel):
    pri_id: Optional[int]
    pri_cellular_number: Optional[str]
    pri_sim_msisdn: Optional[str]
    pri_sim_imsi: Optional[str]
    pri_action: Optional[str]
    pri_level_action: Optional[str]
    pri_status: Optional[str]
    pri_action_date: Optional[str]
    pri_system_date: Optional[str]
    pri_ne_type: Optional[str]
    pri_ne_id: Optional[str]
    pri_ne_service: Optional[str]
    pri_source_application: Optional[str]
    pri_source_app_id: Optional[str]
    pri_sis_id: Optional[str]
    pri_error_code: Optional[str]
    pri_message_error: Optional[str]
    pri_correlation_id: Optional[str]
    pri_reason_code: Optional[str]
    pri_processed_date: Optional[str]
    pri_in_queue: Optional[str]
    pri_response_date: Optional[str]
    pri_delivered_safir: Optional[str]
    pri_received_safir: Optional[str]
    pri_id_sended: Optional[int]
    pri_user_sender: Optional[str]
    pri_ne_entity: Optional[str]
    pri_acc_id: Optional[int]
    pri_main_pri_id: Optional[int]
    pri_resp_manager: Optional[str]
    pri_usr_id: Optional[str]
    pri_priority_usr: Optional[str]
    pri_priority_date: Optional[str]
    pri_save_last_tx_status: Optional[str]
    pri_crm_action: Optional[str]
    pri_request: Optional[str]
    pri_response: Optional[str]
    pri_sended_count: Optional[int]
    pri_main_sis_id: Optional[str]
    pri_imei: Optional[str]
    pri_card_number: Optional[str]
    pri_correlator_id: Optional[str]


class RecordsResponse(BaseModel):
    items: List[RecordItem]
    count: int

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:  # pragma: no cover - FastAPI compatibility
        return super().dict(*args, **kwargs)
