from fastapi import APIRouter, HTTPException, Response
from provisioning_api.schemas.record import RecordsRequest
from provisioning_api.services.records_service import generate_inserts

router = APIRouter()


@router.post("/generate-inserts")
def post_export(body: RecordsRequest):
    try:
        sql = generate_inserts(body.db.model_dump(), body.filters.model_dump())
        return Response(content=sql, media_type="application/sql",
                        headers={"Content-Disposition": "attachment; filename=provisioning_inserts.sql"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
