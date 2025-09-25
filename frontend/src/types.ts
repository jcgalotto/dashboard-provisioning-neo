// frontend/src/types.ts
export type DbCredentials = { host: string; port: number; service: string; user: string; password: string; };
export type Filters = {
  start_date: string; end_date: string; pri_ne_id: string;
  pri_id?: number; pri_action?: string; limit?: number; offset?: number;
};
export type RecordItem = Record<string, string | number | null>;
export type AskAiResponse = { filters: Partial<Filters>; sql: string; errors: string[] };
