import React, { useEffect, useState } from "react";
import { getHistory, getResult } from "../apiClient";
import ResultModal from "./ResultModal";

export default function DiagnosticHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(()=> {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    setLoading(true);
    try {
      const r = await getHistory();
      setHistory(r.data);
    } catch (e) {
      console.error(e);
      alert("Failed to fetch history");
    } finally {
      setLoading(false);
    }
  }

  async function viewResult(id) {
    try {
      const r = await getResult(id);
      setSelected({ id, summary: r.data });
    } catch (e) {
      alert("Failed to fetch result");
    }
  }

  return (
    <div className="bg-card rounded-2xl p-6">
      <h2 className="text-xl font-semibold text-[#00E7FF]">Diagnostic History</h2>
      <p className="text-sm text-[#8B949E] mt-2">All stored diagnostics (latest first)</p>

      <div className="mt-6">
        {loading ? <div className="text-[#8B949E]">Loading...</div> : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left">
              <thead>
                <tr className="text-sm text-[#8B949E]">
                  <th className="py-2 pr-4">API</th>
                  <th className="py-2 pr-4">Type</th>
                  <th className="py-2 pr-4">Time</th>
                  <th className="py-2 pr-4">Status</th>
                  <th className="py-2 pr-4">Vulnerabilities</th>
                  <th className="py-2 pr-4">Action</th>
                </tr>
              </thead>
              <tbody>
                {history.map(h => (
                  <tr key={h.id} className="border-t border-[#20252a]">
                    <td className="py-3 pr-4 w-1/3"><div className="text-sm">{h.url}</div></td>
                    <td className="py-3 pr-4"><div className="text-sm">{h.type}</div></td>
                    <td className="py-3 pr-4"><div className="text-sm text-[#8B949E]">{new Date(h.created_at).toLocaleString()}</div></td>
                    <td className="py-3 pr-4"><div className={`inline-block px-3 py-1 rounded-full text-xs ${h.status==='completed'?'bg-green-800 text-[#39FF14]':'bg-yellow-800 text-[#FFA500]'}`}>{h.status}</div></td>
                    <td className="py-3 pr-4">
                      <div className="text-sm">
                        {(h.summary && h.summary.vulnerabilities && h.summary.vulnerabilities.length>0) ? h.summary.vulnerabilities.join(", ") : "—"}
                      </div>
                    </td>
                    <td className="py-3 pr-4">
                      <button className="px-3 py-1 rounded-lg bg-[#00E7FF] text-black text-sm" onClick={()=>viewResult(h.id)}>View</button>
                    </td>
                  </tr>
                ))}
                {history.length===0 && <tr><td colSpan={6} className="py-6 text-center text-[#8B949E]">No records yet</td></tr>}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <ResultModal result={selected} onClose={()=>setSelected(null)} />
    </div>
  );
}
