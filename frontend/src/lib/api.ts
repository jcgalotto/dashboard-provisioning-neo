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

export function postRecords(payload: any) {
  return postJSON<{ items: any[]; total: number }>('/records', payload);
}

export async function downloadInserts(payload: any) {
  const r = await fetch(`${BASE}/generate-inserts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
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
  return postJSON<import('../types').OptionsResponse>('/options', payload);
}

export const askAi = (text: string) => postJSON('/ai/ask', { text });
