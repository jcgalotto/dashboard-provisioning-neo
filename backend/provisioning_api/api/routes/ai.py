from fastapi import APIRouter
from fastapi import Body
from provisioning_api.ai.graph import run_pipeline

router = APIRouter()


@router.post("/ai/ask")
def ask(payload: dict = Body(...)):
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"filters": {}, "sql": "", "errors": ["Texto vacío."]}
    return run_pipeline(text)
