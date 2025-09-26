from fastapi import APIRouter, HTTPException

from provisioning_api.schemas.record import RecordsRequest
from provisioning_api.db.oracle import connect
from provisioning_api.repositories.options_repository import get_distinct_options

router = APIRouter()


@router.post("/options")
def post_options(body: RecordsRequest):
    """
    Espera en body.db las credenciales y en body.filters al menos:
    - pri_ne_id
    - start_date / end_date
    (pri_id/pri_action etc. se ignoran para los distincts).
    """
    try:
        f = body.filters.model_dump()
        if not f.get("pri_ne_id"):
            raise HTTPException(status_code=422, detail="pri_ne_id es requerido")
        with connect(body.db.model_dump()) as con:
            return get_distinct_options(con, f)
    except HTTPException:
        raise
    except Exception as e:  # pragma: no cover - unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
