import { ApiPayload, AskAiResponse, RecordsResponse } from '../types';

const BASE_URL = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000').replace(/\/$/, '');
const API_URL = `${BASE_URL}/api`;

async function request<T>(path: string, options: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const contentType = response.headers.get('content-type') ?? '';
    if (contentType.includes('application/json')) {
      const data = await response.json().catch(() => null);
      const detail = data?.detail ?? 'Error en la solicitud';
      throw new Error(detail);
    }
    const text = await response.text();
    throw new Error(text || 'Error en la solicitud');
  }

  return response.json() as Promise<T>;
}

export function postRecords(payload: ApiPayload): Promise<RecordsResponse> {
  return request<RecordsResponse>('/records', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function downloadInserts(payload: ApiPayload): Promise<void> {
  const response = await fetch(`${API_URL}/generate-inserts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const contentType = response.headers.get('content-type') ?? '';
    if (contentType.includes('application/json')) {
      const data = await response.json().catch(() => null);
      const detail = data?.detail ?? 'No se pudo generar el archivo de INSERTs';
      throw new Error(detail);
    }
    throw new Error('No se pudo generar el archivo de INSERTs');
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'provisioning_inserts.sql';
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export function askAi(text: string): Promise<AskAiResponse> {
  return request<AskAiResponse>('/ai/ask', {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
}
