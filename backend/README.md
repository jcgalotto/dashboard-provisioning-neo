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

### Conexión a Oracle

- Los servidores Oracle antiguos (11g/12c) suelen requerir modo **THICK**. Instalá Oracle Instant Client 19 u 21 y seteá `FORCE_ORACLE_THICK=1` o dejá que el backend reintente en THICK cuando el driver devuelva `DPY-3010`.
- Si no encuentra el Instant Client, definí `ORACLE_CLIENT_LIB_DIR` (o agregá la carpeta al `PATH`). En Windows necesitás el Microsoft Visual C++ Redistributable 2017-2022 x64 antes de descomprimir el Instant Client.
- Para bases identificadas por **SID**, podés cargar `host:puerto:SID` en el campo "Service"; el backend lo interpretará automáticamente.

### Endpoints principales

- `POST /api/records`
- `POST /api/generate-inserts`
- `POST /api/ai/ask`
