# Backend - Dashboard Provisioning NEO

Este servicio expone una API REST desarrollada con FastAPI que consulta la tabla `swp_provisioning_interfaces` en una base de datos Oracle. Cada petición incluye las credenciales y filtros que se aplican directamente en la consulta, sin almacenar o compartir conexiones entre solicitudes.

## Requisitos

- Python 3.11+
- Dependencias del archivo [`requirements.txt`](requirements.txt)

## Instalación y ejecución

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

La API quedará disponible en `http://localhost:8000`.

## Endpoints

### `POST /records`

Recibe credenciales y filtros, devolviendo una lista paginada de registros y el conteo total.

### `POST /generate-inserts`

Genera un archivo `provisioning_inserts.sql` con sentencias `INSERT` formateadas para todas las filas que cumplan los filtros proporcionados.

## Notas de seguridad

- Las credenciales no se guardan y la conexión se abre y cierra en cada solicitud.
- Todas las entradas se utilizan mediante **binds**, evitando inyección SQL.
- Se validan los formatos de fecha (`YYYY-MM-DD HH:MM:SS`) y la presencia de filtros obligatorios.
