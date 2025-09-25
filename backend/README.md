# Dashboard Provisioning Backend

Backend construido con FastAPI que expone servicios para consultar la tabla `swp_provisioning_interfaces` en Oracle.

## Requisitos

- Python 3.11+
- Dependencias listadas en `requirements.txt`

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn provisioning_api.main:provisioning_api --reload
```

La API queda disponible en `http://localhost:8000` y permite solicitudes desde `http://localhost:5173`.

### Endpoints principales

- `POST /api/records`
- `POST /api/generate-inserts`
- `POST /api/ai/ask`
