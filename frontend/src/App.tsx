import { useMemo, useState } from 'react';

import NLSearch from './components/NLSearch';
import DbForm from './components/DbForm';
import FiltersForm, { sanitizeFilters } from './components/Filters';
import ResultsTable from './components/ResultsTable';
import { askAi, downloadInserts, postRecords } from './lib/api';
import { AskAiResponse, DbCredentials, Filters, RecordItem } from './types';

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
  limit: DEFAULT_LIMIT,
  offset: 0,
};

function sanitize(value: string) {
  return value.trim();
}

export default function App() {
  const [credentials, setCredentials] = useState<DbCredentials>(initialCredentials);
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [items, setItems] = useState<RecordItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState<AskAiResponse | null>(null);

  const normalizedCredentials = useMemo(
    () => ({
      host: sanitize(credentials.host),
      port: credentials.port,
      service: sanitize(credentials.service),
      user: sanitize(credentials.user),
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

    const startDate = sanitize(filters.start_date);
    const endDate = sanitize(filters.end_date);
    const priNeId = sanitize(filters.pri_ne_id);

    if (!startDate || !endDate || !priNeId) {
      return 'Los filtros start_date, end_date y pri_ne_id son obligatorios.';
    }

    if (!DATE_REGEX.test(startDate) || !DATE_REGEX.test(endDate)) {
      return 'El formato de fecha debe ser YYYY-MM-DD HH:MM:SS.';
    }

    return null;
  };

  const buildPayload = (targetPage: number, rawFilters: Filters) => {
    const normalizedFilters: Filters = {
      ...rawFilters,
      start_date: sanitize(rawFilters.start_date),
      end_date: sanitize(rawFilters.end_date),
      pri_ne_id: sanitize(rawFilters.pri_ne_id).toUpperCase(),
      pri_action: rawFilters.pri_action ? String(rawFilters.pri_action).toUpperCase() : rawFilters.pri_action,
      pri_ne_group: rawFilters.pri_ne_group ? String(rawFilters.pri_ne_group).toUpperCase() : rawFilters.pri_ne_group,
      pri_status: rawFilters.pri_status ? String(rawFilters.pri_status).toUpperCase() : rawFilters.pri_status,
    };

    const cleanedFilters = sanitizeFilters(normalizedFilters);
    const limit = cleanedFilters.limit ?? DEFAULT_LIMIT;
    const offset = targetPage * limit;

    return {
      db: normalizedCredentials,
      filters: {
        ...cleanedFilters,
        start_date: sanitize(normalizedFilters.start_date),
        end_date: sanitize(normalizedFilters.end_date),
        pri_ne_id: normalizedFilters.pri_ne_id,
        limit,
        offset,
      },
    };
  };

  const handleSearch = async (targetPage = 0, providedFilters?: Filters) => {
    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    const payload = buildPayload(targetPage, providedFilters ?? filters);

    setLoading(true);
    setError(null);
    try {
      const response = await postRecords(payload);
      setItems(response.items);
      setTotal(response.total);
      setPage(targetPage);
      setFilters((previous) => ({ ...previous, offset: payload.filters.offset, limit: payload.filters.limit }));
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'No se pudieron obtener los registros.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (nextPage: number) => {
    if (nextPage < 0 || nextPage === page) return;
    const limit = filters.limit ?? DEFAULT_LIMIT;
    const maxPage = Math.max(Math.ceil(total / limit) - 1, 0);
    if (nextPage > maxPage) return;
    handleSearch(nextPage);
  };

  const handleGenerateInserts = async (providedFilters?: Filters) => {
    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    const payload = buildPayload(0, providedFilters ?? filters);

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

  const handleAskAi = async (text: string) => {
    setAiLoading(true);
    setError(null);
    try {
      const result = await askAi(text);
      setAiResult(result);
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'No se pudo interpretar la consulta.';
      setError(message);
    } finally {
      setAiLoading(false);
    }
  };

  const handleApplySuggestedFilters = () => {
    if (!aiResult) return;
    setPage(0);
    setFilters((previous) => ({
      ...previous,
      start_date: aiResult.filters.start_date ?? previous.start_date,
      end_date: aiResult.filters.end_date ?? previous.end_date,
      pri_ne_id: aiResult.filters.pri_ne_id
        ? String(aiResult.filters.pri_ne_id).toUpperCase()
        : previous.pri_ne_id,
      pri_id: aiResult.filters.pri_id !== undefined ? Number(aiResult.filters.pri_id) : previous.pri_id,
      pri_action: aiResult.filters.pri_action
        ? String(aiResult.filters.pri_action).toUpperCase()
        : previous.pri_action,
      pri_ne_group: aiResult.filters.pri_ne_group
        ? String(aiResult.filters.pri_ne_group).toUpperCase()
        : previous.pri_ne_group,
      pri_status: aiResult.filters.pri_status
        ? String(aiResult.filters.pri_status).toUpperCase()
        : previous.pri_status,
      offset: 0,
    }));
  };

  return (
    <div className="min-h-screen bg-slate-100 pb-10">
      <header className="bg-indigo-600 py-6 text-white shadow">
        <div className="mx-auto w-full max-w-6xl px-4">
          <h1 className="text-2xl font-semibold">Dashboard Provisioning NEO</h1>
          <p className="mt-1 text-sm text-indigo-100">
            Consulta la tabla swp_provisioning_interfaces, interpreta consultas en texto libre y exporta INSERTs.
          </p>
        </div>
      </header>
      <main className="mx-auto mt-8 w-full max-w-6xl space-y-6 px-4">
        <NLSearch loading={aiLoading} suggestion={aiResult} onAsk={handleAskAi} onApply={handleApplySuggestedFilters} />
        {error && (
          <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        )}
        <DbForm credentials={credentials} onChange={setCredentials} />
        <FiltersForm
          filters={filters}
          credentials={normalizedCredentials}
          onChange={setFilters}
          onSearch={(cleanedFilters) => handleSearch(0, cleanedFilters)}
          onGenerate={(cleanedFilters) => handleGenerateInserts(cleanedFilters)}
          loading={loading}
        />
        <ResultsTable
          items={items}
          total={total}
          limit={filters.limit ?? DEFAULT_LIMIT}
          page={page}
          loading={loading}
          onPageChange={handlePageChange}
        />
      </main>
    </div>
  );
}
