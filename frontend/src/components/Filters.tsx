import { ChangeEvent, useEffect, useState } from 'react';

import { fetchOptions } from '../lib/api';
import { DbCredentials, Filters, OptionsResponse } from '../types';

interface FiltersProps {
  filters: Filters;
  credentials: DbCredentials;
  onChange: (filters: Filters) => void;
  onSearch: () => void;
  onGenerate: () => void;
  loading: boolean;
}

const DATE_PLACEHOLDER = 'YYYY-MM-DD HH:MM:SS';

const EMPTY_OPTIONS: OptionsResponse = { pri_action: [], pri_ne_group: [], pri_status: [] };

export default function FiltersForm({ filters, credentials, onChange, onSearch, onGenerate, loading }: FiltersProps) {
  const [opts, setOpts] = useState<OptionsResponse>(EMPTY_OPTIONS);
  const [loadingOpts, setLoadingOpts] = useState(false);

  useEffect(() => {
    const canLoad = Boolean(filters.pri_ne_id && filters.start_date && filters.end_date);
    if (!canLoad) {
      setOpts(EMPTY_OPTIONS);
      setLoadingOpts(false);
      return;
    }
    let cancelled = false;
    setLoadingOpts(true);
    fetchOptions({
      db: credentials,
      filters: {
        pri_ne_id: filters.pri_ne_id,
        start_date: filters.start_date,
        end_date: filters.end_date,
      },
    })
      .then((response) => {
        if (!cancelled) {
          setOpts(response);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setOpts(EMPTY_OPTIONS);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoadingOpts(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [credentials, filters.pri_ne_id, filters.start_date, filters.end_date]);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    if (name === 'pri_id') {
      const trimmed = value.trim();
      if (!trimmed) {
        onChange({ ...filters, pri_id: undefined });
        return;
      }
      const numeric = Number(trimmed);
      if (!Number.isNaN(numeric)) {
        onChange({ ...filters, pri_id: numeric });
      }
      return;
    }
    onChange({ ...filters, [name]: value });
  };

  return (
    <section className="rounded-lg bg-white p-4 shadow">
      <h2 className="mb-4 text-lg font-semibold text-slate-700">Filtros</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Fecha inicio
          <input
            name="start_date"
            placeholder={DATE_PLACEHOLDER}
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.start_date}
            onChange={handleChange}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Fecha fin
          <input
            name="end_date"
            placeholder={DATE_PLACEHOLDER}
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.end_date}
            onChange={handleChange}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          NE ID
          <input
            name="pri_ne_id"
            placeholder="RCS1"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm uppercase focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_ne_id}
            onChange={handleChange}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          pri_id (opcional)
          <input
            type="number"
            name="pri_id"
            placeholder="123"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_id ?? ''}
            onChange={handleChange}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          pri_action (opcional)
          <select
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm uppercase focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_action ?? ''}
            onChange={(event) =>
              onChange({ ...filters, pri_action: event.target.value || undefined })
            }
            disabled={loadingOpts || !filters.pri_ne_id || !opts.pri_action.length}
          >
            <option value="">Todos</option>
            {opts.pri_action.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          pri_ne_group (opcional)
          <select
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm uppercase focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_ne_group ?? ''}
            onChange={(event) =>
              onChange({ ...filters, pri_ne_group: event.target.value || undefined })
            }
            disabled={loadingOpts || !filters.pri_ne_id || !opts.pri_ne_group.length}
          >
            <option value="">Todos</option>
            {opts.pri_ne_group.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          pri_status (opcional)
          <select
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm uppercase focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_status ?? ''}
            onChange={(event) =>
              onChange({ ...filters, pri_status: event.target.value || undefined })
            }
            disabled={loadingOpts || !filters.pri_ne_id || !opts.pri_status.length}
          >
            <option value="">Todos</option>
            {opts.pri_status.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Cantidad
          <input
            type="number"
            min={1}
            step={1}
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.limit ?? 200}
            onChange={(event) =>
              onChange({
                ...filters,
                limit: Math.max(1, Number(event.target.value || 200)),
              })
            }
          />
        </label>
      </div>
      <div className="mt-6 flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={onSearch}
          disabled={loading}
          className="inline-flex items-center justify-center rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-indigo-300"
        >
          {loading ? 'Buscando…' : 'Buscar'}
        </button>
        <button
          type="button"
          onClick={onGenerate}
          disabled={loading}
          className="inline-flex items-center justify-center rounded border border-indigo-600 px-4 py-2 text-sm font-semibold text-indigo-600 transition hover:bg-indigo-50 disabled:cursor-not-allowed disabled:border-indigo-300 disabled:text-indigo-300"
        >
          Generar INSERTs
        </button>
      </div>
    </section>
  );
}
