const BASE = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api").replace(/\/+$/,"");

async function postJSON<T>(path: string, body: any): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(()=> "");
    throw new Error(`HTTP ${res.status} ${res.statusText}${text? " - " + text : ""}`);
  }
  return res.json() as Promise<T>;
}

export const postRecords = (payload: any) =>
  postJSON<{ items: any[]; total: number }>("/records", payload);

export function fetchOptions(payload: any) {
  // usa el mismo RecordsRequest: db + filters (con pri_ne_id y fechas)
  return postJSON<import("../types").OptionsResponse>("/options", payload);
}

export async function downloadInserts(payload: any) {
  const res = await fetch(`${BASE}/generate-inserts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "provisioning_inserts.sql"; a.click();
  URL.revokeObjectURL(url);
}

export const askAi = (text: string) => postJSON<{filters:any; sql:string; errors:string[]}>("/ai/ask", { text });
