import { ChangeEvent } from 'react';

import { DbCredentials } from '../types';

interface DbFormProps {
  credentials: DbCredentials;
  onChange: (credentials: DbCredentials) => void;
}

export default function DbForm({ credentials, onChange }: DbFormProps) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    if (name === 'port') {
      const numericValue = Number(value);
      onChange({ ...credentials, [name]: Number.isNaN(numericValue) ? 0 : numericValue });
    } else {
      onChange({ ...credentials, [name]: value });
    }
  };

  return (
    <section className="rounded-lg bg-white p-4 shadow">
      <h2 className="mb-4 text-lg font-semibold text-slate-700">Credenciales Oracle</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Host
          <input
            name="host"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={credentials.host}
            onChange={handleChange}
            placeholder="localhost"
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Puerto
          <input
            name="port"
            type="number"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={credentials.port}
            onChange={handleChange}
            placeholder="1521"
            min={1}
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Service
          <input
            name="service"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={credentials.service}
            onChange={handleChange}
            placeholder="xe"
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Usuario
          <input
            name="user"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={credentials.user}
            onChange={handleChange}
            placeholder="usuario"
          />
        </label>
        <label className="flex flex-col text-sm font-medium text-slate-600">
          Password
          <input
            name="password"
            type="password"
            className="mt-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring"
            value={credentials.password}
            onChange={handleChange}
            placeholder="********"
          />
        </label>
      </div>
    </section>
  );
}
