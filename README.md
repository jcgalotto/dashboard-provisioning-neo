# Dashboard Provisioning NEO

Aplicación full-stack que permite consultar, exportar y analizar registros de la tabla `swp_provisioning_interfaces` en Oracle. El
frontend está construido con React + Vite + TypeScript + Tailwind y el backend con FastAPI, siguiendo una arquitectura por capas y
soporte de consultas en lenguaje natural con LangGraph.

## Estructura del repositorio

```
dashboard-provisioning-neo/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ schemas/
│  │  ├─ utils/
│  │  ├─ services/
│  │  ├─ repositories/
│  │  ├─ api/
│  │  └─ ai/
│  ├─ requirements.txt
│  └─ README.md
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ vite.config.ts
│  ├─ tailwind.config.js
│  ├─ postcss.config.js
│  └─ src/
│     ├─ main.tsx
│     ├─ App.tsx
│     ├─ styles.css
│     ├─ lib/api.ts
│     ├─ types.ts
│     └─ components/
│        ├─ DbForm.tsx
│        ├─ Filters.tsx
│        ├─ ResultsTable.tsx
│        └─ NLSearch.tsx
└─ README.md
```

## Puesta en marcha

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn provisioning_api.main:provisioning_api --reload
```

La API queda disponible en `http://localhost:8000`.

> ℹ️ **Conexión a Oracle**
>
> - Las bases de datos antiguas (por ejemplo 11g/12c sin parches recientes) requieren el modo **THICK**, que necesita Oracle Instant Client 19 u 21. Activá el modo thick seteando `FORCE_ORACLE_THICK=1` o dejá que la API cambie automáticamente cuando el driver devuelva `DPY-3010`.
> - Si el servidor exige modo THICK y no encuentra las librerías nativas, instalá Oracle Instant Client y apuntá `ORACLE_CLIENT_LIB_DIR` al directorio donde lo descomprimiste (también podés agregarlo al `PATH`). En Windows es obligatorio instalar el **Microsoft Visual C++ Redistributable 2017-2022 x64**, descomprimir el Instant Client y luego reiniciar la terminal.
> - Cuando la base publica un **SID** en lugar de un service name, podés cargar `host:puerto:SID` directamente en el campo “Service”; la API ajustará los parámetros al conectarse.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación web se sirve en `http://localhost:5173` y se comunica con el backend a través de `http://localhost:8000/api` (configu
rable mediante `VITE_API_URL`).

## Funcionalidades principales

1. **Consulta paginada:** filtros obligatorios `start_date`, `end_date`, `pri_ne_id` y opcionales `pri_id`, `pri_action`.
2. **Exportación de INSERTs:** genera un archivo `provisioning_inserts.sql` con las filas filtradas aplicando reglas de negocio.
3. **Búsqueda en lenguaje natural:** interpreta texto libre, propone filtros y muestra el SQL generado.

Las credenciales de Oracle se envían en cada request y no se almacenan en el servidor. La conexión usa `python-oracledb` en modo
thin con `fetch_lobs=False` para optimizar la transferencia de datos.
