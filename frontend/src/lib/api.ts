import type { AskAiResponse, OptionsResponse } from '../types';

const BASE = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api').replace(/\/+$/, '');

async function postJSON<T>(path: string, body: any): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const text = await r.text().catch(() => '');
    throw new Error(text || `HTTP ${r.status}`);
  }
  return r.json() as Promise<T>;
}

function scrub(body: any) {
  const filters = body?.filters ?? {};
  const cleaned: Record<string, unknown> = {};
  Object.entries(filters).forEach(([key, value]) => {
    if (value === '' || value === 'TODOS' || value === null || value === undefined) {
      return;
    }
    if (key === 'pri_id') {
      const numeric = Number(value);
      if (!Number.isNaN(numeric)) {
        cleaned[key] = numeric;
      }
      return;
    }
    if (key === 'limit') {
      const numericLimit = Math.max(1, parseInt(String(value), 10));
      cleaned[key] = numericLimit;
      return;
    }
    cleaned[key] = value;
  });
  return { ...body, filters: { ...cleaned } };
}

export function postRecords(payload: any) {
  return postJSON<{ items: any[]; total: number }>('/records', scrub(payload));
}

export async function downloadInserts(payload: any) {
  const cleanPayload = scrub(payload);
  const r = await fetch(`${BASE}/generate-inserts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cleanPayload),
  });
  if (!r.ok) {
    const text = await r.text().catch(() => '');
    throw new Error(text || `HTTP ${r.status}`);
  }
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'provisioning_inserts.sql';
  a.click();
  URL.revokeObjectURL(url);
}

export function fetchOptions(payload: any) {
  return postJSON<OptionsResponse>('/options', payload);
}

export const askAi = (text: string) => postJSON<AskAiResponse>('/ai/ask', { text });
