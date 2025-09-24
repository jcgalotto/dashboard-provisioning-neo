import { useMemo, useState } from 'react';

import DbForm from './components/DbForm';
import FiltersForm from './components/Filters';
import ResultsTable from './components/ResultsTable';
import { downloadInserts, fetchRecords } from './lib/api';
import { DbCredentials, Filters, RecordItem } from './types';

const DEFAULT_LIMIT = 200;
const DATE_REGEX = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;

const initialCredentials: DbCredentials = {
  host: '',
  port: 1521,
  service: '',
  user: '',
  password: '',
};

const initialFilters: Filters = {
  start_date: '',
  end_date: '',
  pri_ne_id: '',
  pri_id: '',
  pri_action: '',
};

function sanitizeString(value: string) {
  return value.trim();
}

export default function App() {
  const [credentials, setCredentials] = useState<DbCredentials>(initialCredentials);
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [items, setItems] = useState<RecordItem[]>([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const normalizedCredentials = useMemo(
    () => ({
      host: sanitizeString(credentials.host),
      port: credentials.port,
      service: sanitizeString(credentials.service),
      user: sanitizeString(credentials.user),
      password: credentials.password,
    }),
    [credentials],
  );

  const validateInputs = (): string | null => {
    if (!normalizedCredentials.host || !normalizedCredentials.service || !normalizedCredentials.user || !normalizedCredentials.password) {
      return 'Complete todas las credenciales de conexión.';
    }

    if (!normalizedCredentials.port || Number.isNaN(normalizedCredentials.port) || normalizedCredentials.port <= 0) {
      return 'El puerto debe ser un número mayor a 0.';
    }

    const startDate = sanitizeString(filters.start_date);
    const endDate = sanitizeString(filters.end_date);
    const priNeId = sanitizeString(filters.pri_ne_id);

    if (!startDate || !endDate || !priNeId) {
      return 'Los filtros start_date, end_date y pri_ne_id son obligatorios.';
    }

    if (!DATE_REGEX.test(startDate) || !DATE_REGEX.test(endDate)) {
      return 'El formato de fecha debe ser YYYY-MM-DD HH:MM:SS.';
    }

    if (filters.pri_id && Number.isNaN(Number(filters.pri_id))) {
      return 'pri_id debe ser numérico.';
    }

    return null;
  };

  const buildPayload = (targetPage: number) => {
    const priAction = sanitizeString(filters.pri_action ?? '');
    const priIdValue = sanitizeString(filters.pri_id ?? '');

    return {
      db: normalizedCredentials,
      filters: {
        start_date: sanitizeString(filters.start_date),
        end_date: sanitizeString(filters.end_date),
        pri_ne_id: sanitizeString(filters.pri_ne_id),
        ...(priIdValue ? { pri_id: Number(priIdValue) } : {}),
        ...(priAction ? { pri_action: priAction } : {}),
        limit: DEFAULT_LIMIT,
        offset: targetPage * DEFAULT_LIMIT,
      },
    };
  };

  const handleSearch = async (targetPage = 0) => {
    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    const payload = buildPayload(targetPage);

    setLoading(true);
    setError(null);
    try {
      const response = await fetchRecords(payload);
      setItems(response.items);
      setCount(response.count);
      setPage(targetPage);
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'No se pudieron obtener los registros.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (nextPage: number) => {
    if (nextPage < 0 || nextPage === page) return;
    handleSearch(nextPage);
  };

  const handleGenerateInserts = async () => {
    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    const payload = buildPayload(0);

    setLoading(true);
    setError(null);
    try {
      await downloadInserts(payload);
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'No se pudo generar el archivo de INSERTs.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 pb-10">
      <header className="bg-indigo-600 py-6 text-white shadow">
        <div className="mx-auto w-full max-w-6xl px-4">
          <h1 className="text-2xl font-semibold">Dashboard Provisioning NEO</h1>
          <p className="mt-1 text-sm text-indigo-100">
            Consulta la tabla swp_provisioning_interfaces y exporta los resultados como INSERTs SQL.
          </p>
        </div>
      </header>
      <main className="mx-auto mt-8 w-full max-w-6xl space-y-6 px-4">
        {error && (
          <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}
        <DbForm credentials={credentials} onChange={setCredentials} />
        <FiltersForm filters={filters} onChange={setFilters} onSearch={() => handleSearch(0)} onGenerate={handleGenerateInserts} loading={loading} />
        <ResultsTable items={items} count={count} limit={DEFAULT_LIMIT} page={page} loading={loading} onPageChange={handlePageChange} />
      </main>
    </div>
  );
}
