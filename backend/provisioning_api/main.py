from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..provisioning_api.api.routes.records import router as records_router
from ..provisioning_api.api.routes.export  import router as export_router
from ..provisioning_api.api.routes.ai      import router as ai_router
from ..provisioning_api.core.config        import get_settings
from ..provisioning_api.core.logging       import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(title="Dashboard Provisioning API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(records_router, prefix=settings.api_prefix)
app.include_router(export_router,  prefix=settings.api_prefix)
app.include_router(ai_router,      prefix=settings.api_prefix)
