import React, { useState, useRef } from "react";
import { startTest, getStatus, getResult } from "../apiClient";
import ProgressModal from "./ProgressModal";
import ResultModal from "./ResultModal";
import { motion } from "framer-motion";

function detectTargetType(value) {
  const ipRegex =
    /^(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$/;

  try {
    const parsed = new URL(value);
    const host = parsed.hostname;

    if (ipRegex.test(host)) {
      return "IP Address";
    }
    return "Domain API";
  } catch {
    return "";
  }
}

export default function DiagnosticTool() {
    const [url, setUrl] = useState("");
    const [apiKey, setApiKey] = useState("");
    const [authType, setAuthType] = useState("none");
    const [type, setType] = useState("basic");
  const [runningTask, setRunningTask] = useState(null);
  const [progress, setProgress] = useState(0);
  const [showProgress, setShowProgress] = useState(false);
  const [result, setResult] = useState(null);
  const pollRef = useRef(null);
  const [targetType, setTargetType] = useState("");

  async function handleStart() {
    if (!url) return alert("Enter API URL or endpoint to test.");
    try {
      const resp = await startTest({
        url,
        type,
        apiKey,
        authType
      });
      const taskId = resp.data.task_id;
      setRunningTask(taskId);
      setShowProgress(true);
      setProgress(2);
      pollStatus(taskId);
    } catch (e) {
      alert("Failed to start test: " + (e?.response?.data?.error || e.message));
    }
  }

  async function pollStatus(taskId) {
    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      try {
        const s = await getStatus(taskId);
        const data = s.data;
        setProgress(data.progress || 0);
        if (data.status === "completed" || data.status === "failed") {
          clearInterval(pollRef.current);
          setShowProgress(false);
          const r = await getResult(taskId);
          setResult({ id: taskId, summary: r.data });
          setRunningTask(null);
        }
      } catch (e) {
        console.error("poll error", e);
      }
    }, 1400);
  }

  function handleCancel() {
    // backend cancel endpoint not implemented here; show feedback
    if (runningTask) {
      // best-effort: stop polling locally
      if (pollRef.current) clearInterval(pollRef.current);
      setShowProgress(false);
      setRunningTask(null);
      setProgress(0);
      alert("Cancellation requested locally.");
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-card rounded-2xl p-6 shadow-md">
        <h2 className="text-xl font-semibold text-[#00E7FF]">Diagnostic Tool</h2>
        <p className="text-sm text-[#8B949E] mt-2">One-click checkup or customize with fuzz test.</p>

        <div className="mt-6 space-y-4">
          <div>
            <label className="text-sm text-[#8B949E]">API URL / Endpoint</label>
            <input value={url} onChange={(e) => {
                const value = e.target.value;
                setUrl(value);
                setTargetType(detectTargetType(value));
                }} placeholder="https://api.example.com/v1/health"
              className="w-full mt-2 p-3 rounded-xl bg-[#0b1220] outline-none border border-[#263038]" />
          </div>

          {targetType && (
  <p className="text-xs text-[#8B949E] mt-2">
    Detected Target Type: {targetType}
  </p>
)}
    <div>
        <label className="text-sm text-[#8B949E]">API Key (optional)</label>
            <input
                value={apiKey}
                onChange={e => setApiKey(e.target.value)}
                placeholder="Enter API key if required"
                className="w-full mt-2 p-3 rounded-xl bg-[#0b1220] outline-none border border-[#263038]" />
    </div>

        <div>
            <label className="text-sm text-[#8B949E]">Authentication Type</label>
                <select
                    value={authType}
                    onChange={e => setAuthType(e.target.value)}
                    className="w-full mt-2 p-3 rounded-xl bg-[#0b1220] border border-[#263038]">
                <option value="none">None</option>
                <option value="header">Header API Key</option>
                <option value="query">Query Parameter</option>
            </select>
        </div>

          <div>
            <label className="text-sm text-[#8B949E]">Test Type</label>
            <select value={type} onChange={e=>setType(e.target.value)}
              className="w-full mt-2 p-3 rounded-xl bg-[#0b1220] border border-[#263038]">
              <option value="basic">One-click Diagnosis </option>
              <option value="fuzz">Fuzz Test </option>
              <option value="stress">Stress Test </option>
              <option value="bola">BOLA Authorization Test</option>
            </select>
          </div>

          <div className="flex items-center space-x-3">
            <motion.button
              onClick={handleStart}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-3 rounded-2xl bg-[#00E7FF] text-black font-medium"
            >
              Run Checkup
            </motion.button>

            <button onClick={()=>{ setUrl("");
                setApiKey("");
                setAuthType("none");
                setType("basic");
                setTargetType(""); }} className="px-4 py-2 rounded-2xl bg-[#111418] border border-[#263038]">
              Reset
            </button>
          </div>

          <div className="text-sm text-[#8B949E]">
            <strong>Note:</strong> Fuzz test send multiple requests. Only test APIs you own or have permission to test.
          </div>
        </div>
      </div>

      <div className="bg-card rounded-2xl p-6 shadow-md">
        <h3 className="text-lg font-semibold text-[#00E7FF]">Recent Activity</h3>
        <p className="text-sm text-[#8B949E] mt-2">Quick access to last 5 checks from backend history.</p>

        <RecentHistory previewCount={5} onShowResult={(r)=>setResult(r)} />

      </div>

      <ProgressModal open={showProgress} progress={progress} onCancel={handleCancel} />
      {result && <ResultModal result={result} onClose={()=>setResult(null)} />}
    </div>
  );
}

/* small helper component */
function RecentHistory({ previewCount=5, onShowResult }) {
  const [items, setItems] = React.useState([]);
  React.useEffect(()=> {
    let mounted=true;
    import("../apiClient").then(mod => mod.getHistory()).then(r=> {
      if(!mounted) return;
      setItems(r.data.slice(0, previewCount));
    }).catch(()=>{});
    return ()=> mounted=false;
  }, []);
  return (
    <div className="mt-4">
      <ul className="space-y-3">
        {items.length===0 && <li className="text-sm text-[#8B949E]">No history yet</li>}
        {items.map(it => (
          <li key={it.id} className="p-3 bg-[#0b1220] rounded-xl border border-[#262b31] flex justify-between items-center">
            <div>
              <div className="text-sm font-medium">{it.url}</div>
              <div className="text-xs text-[#8B949E]">{it.type} • {new Date(it.created_at).toLocaleString()}</div>
            </div>
            <div className="flex items-center space-x-2">
              <button onClick={()=> onShowResult({ id: it.id, summary: it.summary })} className="px-3 py-1 rounded-lg bg-[#00E7FF] text-black text-sm">Result</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
