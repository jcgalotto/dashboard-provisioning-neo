import uvicorn
from provisioning_api.core.config import get_settings

if __name__ == "__main__":
    s = get_settings()
    uvicorn.run("provisioning_api.main:app", host=s.uvicorn_host, port=s.uvicorn_port, reload=True)
