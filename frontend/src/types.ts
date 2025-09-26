export type DbCredentials = { host: string; port: number; service: string; user: string; password: string; };
export type Filters = {
  start_date: string; end_date: string; pri_ne_id: string;
  pri_id?: number; pri_action?: string; pri_ne_group?: string; pri_status?: string;
  limit?: number; offset?: number;
};
export type OptionsResponse = {
  pri_action: string[];
  pri_ne_group: string[];
  pri_status: string[];
};
export type RecordItem = Record<string, string | number | null>;
export type AskAiResponse = {
  filters: {
    start_date?: string; end_date?: string; pri_ne_id?: string | number;
    pri_id?: string | number; pri_action?: string; pri_ne_group?: string; pri_status?: string;
    limit?: number; offset?: number;
  };
  sql: string; errors: string[];
};
