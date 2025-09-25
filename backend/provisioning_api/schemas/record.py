"""Pydantic models for provisioning records."""
from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, Field, ValidationInfo, field_validator

Num = Union[int, float, str]


class Record(BaseModel):
    """Represents a provisioning interface row."""

    pri_id: Optional[Num] = None
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
    pri_source_app_id: Optional[Num] = None
    pri_sis_id: Optional[Num] = None
    pri_error_code: Optional[str] = None
    pri_message_error: Optional[str] = None
    pri_correlation_id: Optional[Num] = None
    pri_reason_code: Optional[str] = None
    pri_processed_date: Optional[str] = None
    pri_response_date: Optional[str] = None
    pri_priority_date: Optional[str] = None
    pri_in_queue: Optional[str] = None
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
    """Response payload containing records and total count."""

    items: list[Record]
    total: int


class DBParams(BaseModel):
    """Oracle connection parameters."""

    host: str
    port: int
    service: str
    user: str
    password: str


class Filters(BaseModel):
    """Query filters for retrieving provisioning records."""

    start_date: str = Field(..., description="YYYY-MM-DD HH:MM:SS")
    end_date: str = Field(..., description="YYYY-MM-DD HH:MM:SS")
    pri_ne_id: str
    pri_id: Optional[Num] = None
    pri_action: Optional[str] = None
    limit: int = 100
    offset: int = 0

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_datetime_format(cls, value: str) -> str:
        """Ensure the provided value matches the required datetime format."""

        try:
            date_part, time_part = value.split(" ")
            year, month, day = date_part.split("-")
            hour, minute, second = time_part.split(":")
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("Formato de fecha inválido, use YYYY-MM-DD HH:MM:SS") from exc

        if not (
            len(year) == 4
            and len(month) == 2
            and len(day) == 2
            and len(hour) == 2
            and len(minute) == 2
            and len(second) == 2
        ):
            raise ValueError("Formato de fecha inválido, use YYYY-MM-DD HH:MM:SS")

        return value

    @field_validator('limit', 'offset')
    @classmethod
    def validate_positive(cls, value: int, info: ValidationInfo) -> int:
        """Ensure pagination values are non-negative."""

        if value < 0:
            raise ValueError(f"{info.field_name} debe ser mayor o igual a 0")
        return value


class RecordsRequest(BaseModel):
    """Full request payload containing DB params and filters."""

    db: DBParams
    filters: Filters
