import React from "react";
import { motion } from "framer-motion";

export default function ResultModal({ result, onClose }) {
  if (!result) return null;
  const r = result.summary || result;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose}></div>
      <motion.div initial={{scale:0.98, opacity:0}} animate={{scale:1, opacity:1}} className="relative bg-card rounded-2xl p-6 w-11/12 max-w-3xl">
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-semibold text-[#00E7FF]">Diagnostic Result</h3>
          <button onClick={onClose} className="text-sm text-[#8B949E]">Close</button>
        </div>

        <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div>
            <h4 className="text-sm text-[#8B949E]">Summary</h4>
            <pre className="mt-2 p-3 bg-[#0b1220] rounded-md overflow-auto">{JSON.stringify(r.summary || r, null, 2)}</pre>
          </div>

          <div>
            <h4 className="text-sm text-[#8B949E]">Vulnerabilities & Suggestions</h4>
            <div className="mt-2 space-y-2">
              { (r.vulnerabilities && r.vulnerabilities.length>0) ? r.vulnerabilities.map((v,i)=>(
                <div key={i} className="p-3 bg-[#0b1220] rounded-md border border-[#262b31]">
                  <div className="text-sm font-medium">{v}</div>
                  <div className="text-xs text-[#8B949E] mt-1">Suggestion: Check input validation, headers, and server config.</div>
                </div>
              )) : <div className="text-sm text-[#8B949E]">No vulnerabilities detected (quick heuristic).</div>}
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-between">

  <a
  href={`http://127.0.0.1:5000/api/report/${result.id}`}
  target="_blank"
  rel="noopener noreferrer"
  className="px-4 py-2 rounded-2xl bg-[#00E7FF] text-black"
>
  Download Report
</a>

  <a
    href="#"
    onClick={(e)=>{ e.preventDefault(); onClose(); }}
    className="px-4 py-2 rounded-2xl bg-[#111418] border border-[#263038]"
  >
    Done
  </a>

</div>
      </motion.div>
    </div>
  );
}
