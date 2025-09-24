import { ApiPayload, RecordsResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      const detail = data?.detail ?? 'Error en la solicitud';
      throw new Error(detail);
    }
    const text = await response.text();
    throw new Error(text || 'Error en la solicitud');
  }
  return response.json() as Promise<T>;
}

export async function fetchRecords(payload: ApiPayload): Promise<RecordsResponse> {
  const response = await fetch(`${API_BASE_URL}/records`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  return handleResponse<RecordsResponse>(response);
}

export async function downloadInserts(payload: ApiPayload): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/generate-inserts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail ?? 'No se pudo generar el archivo de INSERTs';
    throw new Error(detail);
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
