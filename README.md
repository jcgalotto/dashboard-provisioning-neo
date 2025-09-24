# Dashboard Provisioning NEO

Aplicación full-stack que permite consultar y exportar registros de la tabla `swp_provisioning_interfaces` en Oracle. Incluye un frontend en React + Vite + Tailwind y un backend en FastAPI que se conecta a Oracle con `python-oracledb` (modo thin).

## Estructura del repositorio

```
dashboard-provisioning-neo/
├─ backend/
│  ├─ app.py
│  ├─ db.py
│  ├─ models.py
│  ├─ queries.py
│  ├─ utils_sql.py
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
│        └─ ResultsTable.tsx
└─ README.md
```

## Puesta en marcha

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación web quedará disponible en `http://localhost:5173` y consumirá la API expuesta por el backend (`http://localhost:8000`).

## Uso

1. Ingresa las credenciales de Oracle (host, port, service, user, password).
2. Completa los filtros obligatorios (`start_date`, `end_date`, `pri_ne_id`) y opcionalmente `pri_id` y `pri_action`.
3. Presiona **Buscar** para cargar los registros paginados (limit `200`, offset controlado desde la UI).
4. Presiona **Generar INSERTs** para descargar un archivo `provisioning_inserts.sql` con las filas que cumplen los filtros actuales.

Todos los valores se envían al backend en cada solicitud y nunca se almacenan en el frontend ni en el servidor.
