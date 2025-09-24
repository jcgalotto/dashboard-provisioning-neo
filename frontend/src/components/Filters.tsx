import { ChangeEvent } from 'react';

import { Filters } from '../types';

interface FiltersProps {
  filters: Filters;
  onChange: (filters: Filters) => void;
  onSearch: () => void;
  onGenerate: () => void;
  loading: boolean;
}

const DATE_PLACEHOLDER = 'YYYY-MM-DD HH:MM:SS';

export default function FiltersForm({ filters, onChange, onSearch, onGenerate, loading }: FiltersProps) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
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
            name="pri_id"
            placeholder="123"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_id ?? ''}
            onChange={handleChange}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          pri_action (opcional)
          <input
            name="pri_action"
            placeholder="ALTA"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm uppercase focus:border-indigo-500 focus:outline-none focus:ring"
            value={filters.pri_action ?? ''}
            onChange={handleChange}
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
