import { RecordItem } from '../types';

interface ResultsTableProps {
  items: RecordItem[];
  count: number;
  limit: number;
  page: number;
  loading: boolean;
  onPageChange: (page: number) => void;
}

const columns: { key: keyof RecordItem; label: string }[] = [
  { key: 'pri_id', label: 'pri_id' },
  { key: 'pri_cellular_number', label: 'pri_cellular_number' },
  { key: 'pri_sim_msisdn', label: 'pri_sim_msisdn' },
  { key: 'pri_sim_imsi', label: 'pri_sim_imsi' },
  { key: 'pri_action', label: 'pri_action' },
  { key: 'pri_level_action', label: 'pri_level_action' },
  { key: 'pri_status', label: 'pri_status' },
  { key: 'pri_action_date', label: 'pri_action_date' },
  { key: 'pri_system_date', label: 'pri_system_date' },
  { key: 'pri_ne_type', label: 'pri_ne_type' },
  { key: 'pri_ne_id', label: 'pri_ne_id' },
  { key: 'pri_ne_service', label: 'pri_ne_service' },
  { key: 'pri_source_application', label: 'pri_source_application' },
  { key: 'pri_source_app_id', label: 'pri_source_app_id' },
  { key: 'pri_sis_id', label: 'pri_sis_id' },
  { key: 'pri_error_code', label: 'pri_error_code' },
  { key: 'pri_message_error', label: 'pri_message_error' },
  { key: 'pri_correlation_id', label: 'pri_correlation_id' },
  { key: 'pri_reason_code', label: 'pri_reason_code' },
  { key: 'pri_processed_date', label: 'pri_processed_date' },
  { key: 'pri_in_queue', label: 'pri_in_queue' },
  { key: 'pri_response_date', label: 'pri_response_date' },
  { key: 'pri_delivered_safir', label: 'pri_delivered_safir' },
  { key: 'pri_received_safir', label: 'pri_received_safir' },
  { key: 'pri_id_sended', label: 'pri_id_sended' },
  { key: 'pri_user_sender', label: 'pri_user_sender' },
  { key: 'pri_ne_entity', label: 'pri_ne_entity' },
  { key: 'pri_acc_id', label: 'pri_acc_id' },
  { key: 'pri_main_pri_id', label: 'pri_main_pri_id' },
  { key: 'pri_resp_manager', label: 'pri_resp_manager' },
  { key: 'pri_usr_id', label: 'pri_usr_id' },
  { key: 'pri_priority_usr', label: 'pri_priority_usr' },
  { key: 'pri_priority_date', label: 'pri_priority_date' },
  { key: 'pri_save_last_tx_status', label: 'pri_save_last_tx_status' },
  { key: 'pri_crm_action', label: 'pri_crm_action' },
  { key: 'pri_request', label: 'pri_request' },
  { key: 'pri_response', label: 'pri_response' },
  { key: 'pri_sended_count', label: 'pri_sended_count' },
  { key: 'pri_main_sis_id', label: 'pri_main_sis_id' },
  { key: 'pri_imei', label: 'pri_imei' },
  { key: 'pri_card_number', label: 'pri_card_number' },
  { key: 'pri_correlator_id', label: 'pri_correlator_id' },
];

export default function ResultsTable({ items, count, limit, page, loading, onPageChange }: ResultsTableProps) {
  const start = page * limit + (items.length > 0 ? 1 : 0);
  const end = page * limit + items.length;
  const hasPrevious = page > 0;
  const hasNext = (page + 1) * limit < count;

  return (
    <section className="rounded-lg bg-white p-4 shadow">
      <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-lg font-semibold text-slate-700">Resultados</h2>
        <p className="text-sm text-slate-500">
          {loading
            ? 'Cargando…'
            : count > 0
            ? `Mostrando ${start}-${end} de ${count} registros`
            : 'Sin resultados'}
        </p>
      </div>
      <div className="max-h-[480px] overflow-auto rounded border border-slate-200">
        <table className="min-w-full table-auto text-left text-xs">
          <thead className="sticky top-0 bg-slate-100">
            <tr>
              {columns.map((column) => (
                <th key={column.key as string} className="px-3 py-2 font-semibold uppercase tracking-wide text-slate-600">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-3 py-6 text-center text-sm text-slate-500">
                  {loading ? 'Cargando…' : 'No hay registros que coincidan con los filtros.'}
                </td>
              </tr>
            ) : (
              items.map((item, rowIndex) => (
                <tr key={`${item.pri_id ?? rowIndex}-${rowIndex}`} className="odd:bg-white even:bg-slate-50">
                  {columns.map((column) => {
                    const value = item[column.key];
                    const displayValue = value ?? '';
                    return (
                      <td key={column.key as string} className="max-w-[220px] px-3 py-2 align-top">
                        <span className="block truncate" title={displayValue?.toString()}>
                          {displayValue}
                        </span>
                      </td>
                    );
                  })}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex flex-col items-start gap-2 sm:flex-row sm:items-center sm:justify-between">
        <span className="text-xs text-slate-500">Límite por página: {limit}</span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onPageChange(page - 1)}
            disabled={!hasPrevious || loading}
            className="rounded border border-slate-300 px-3 py-1 text-sm font-medium text-slate-600 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Anterior
          </button>
          <span className="text-xs text-slate-500">Página {page + 1}</span>
          <button
            type="button"
            onClick={() => onPageChange(page + 1)}
            disabled={!hasNext || loading}
            className="rounded border border-slate-300 px-3 py-1 text-sm font-medium text-slate-600 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Siguiente
          </button>
        </div>
      </div>
    </section>
  );
}
