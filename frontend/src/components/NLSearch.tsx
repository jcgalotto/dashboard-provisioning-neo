import { FormEvent, useMemo, useState } from 'react';

import { AskAiResponse } from '../types';

interface NLSearchProps {
  loading: boolean;
  suggestion: AskAiResponse | null;
  onAsk: (text: string) => Promise<void>;
  onApply: () => void;
}

export default function NLSearch({ loading, suggestion, onAsk, onApply }: NLSearchProps) {
  const [text, setText] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  const cleanedFilters = useMemo(() => {
    if (!suggestion) return {} as Record<string, unknown>;
    return Object.fromEntries(
      Object.entries(suggestion.filters ?? {}).filter(
        ([key]) => !['limit', 'offset'].includes(key),
      ),
    );
  }, [suggestion]);

  const hasSuggestion = Object.keys(cleanedFilters).length > 0;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!text.trim()) {
      setLocalError('Ingresa una consulta en texto libre.');
      return;
    }
    setLocalError(null);
    await onAsk(text.trim());
  };

  return (
    <section className="rounded-lg bg-white p-4 shadow">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="mb-2 block text-sm font-semibold text-slate-700" htmlFor="nl-textarea">
            Búsqueda en lenguaje natural
          </label>
          <textarea
            id="nl-textarea"
            rows={3}
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Ej: Alta en RCS1 entre ayer y hoy para pri_id 123"
            className="w-full rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
          />
        </div>
        {localError && <p className="text-sm text-red-600">{localError}</p>}
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:bg-emerald-300"
          >
            {loading ? 'Interpretando…' : 'Interpretar consulta'}
          </button>
          {hasSuggestion && (
            <button
              type="button"
              onClick={onApply}
              disabled={loading || (suggestion?.errors?.length ?? 0) > 0}
              className="inline-flex items-center justify-center rounded border border-emerald-600 px-4 py-2 text-sm font-semibold text-emerald-700 transition hover:bg-emerald-50 disabled:cursor-not-allowed disabled:border-emerald-200 disabled:text-emerald-300"
            >
              Aplicar filtros sugeridos
            </button>
          )}
        </div>
      </form>
      {suggestion && (
        <div className="mt-4 space-y-3 text-sm">
          <div>
            <h3 className="font-semibold text-slate-700">Filtros sugeridos</h3>
            {hasSuggestion ? (
              <ul className="mt-2 grid gap-2 sm:grid-cols-2">
                {Object.entries(cleanedFilters).map(([key, value]) => (
                  <li key={key} className="rounded border border-slate-200 bg-slate-50 px-3 py-2">
                    <span className="font-medium text-slate-600">{key}</span>:{' '}
                    <span className="text-slate-700">{String(value)}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-slate-500">No se pudieron derivar filtros.</p>
            )}
          </div>
          {suggestion.sql && (
            <div>
              <h3 className="font-semibold text-slate-700">SQL generado</h3>
              <pre className="mt-2 max-h-48 overflow-auto rounded bg-slate-900 p-3 text-xs text-slate-100">
                <code>{suggestion.sql}</code>
              </pre>
            </div>
          )}
          {suggestion.errors.length > 0 && (
            <div>
              <h3 className="font-semibold text-slate-700">Observaciones</h3>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-red-600">
                {suggestion.errors.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
