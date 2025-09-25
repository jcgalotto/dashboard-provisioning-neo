from fastapi import APIRouter, HTTPException
from provisioning_api.schemas.record import RecordsRequest, RecordsResponse, Record
from provisioning_api.services.records_service import get_records

router = APIRouter()


@router.post("/records", response_model=RecordsResponse)
def post_records(body: RecordsRequest):
    try:
        items, total = get_records(body.db.model_dump(), body.filters.model_dump())
        return {"items": [Record(**r) for r in items], "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
