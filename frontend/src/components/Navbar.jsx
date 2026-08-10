import React from "react";
import { FiActivity, FiList } from "react-icons/fi";

export default function Navbar({ active, onChange }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="rounded-2xl p-2 bg-gradient-to-br from-[#071421] to-[#0b1720]">
          <h1 className="text-2xl font-bold text-[#00E7FF]">R. A. P. I. D. Resilient API Diagnostics</h1>
        </div>
        <p className="text-sm text-[#8B949E] ml-2">Because every microsecond matters in security</p>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={() => onChange("tool")}
          className={`flex items-center px-4 py-2 rounded-2xl ${active === "tool" ? "bg-[#0b2b3a] ring-1 ring-[#00E7FF]" : "bg-[#11161b]"}`}
        >
          <FiActivity className="mr-2" /> Diagnostic Tool
        </button>

        <button
          onClick={() => onChange("history")}
          className={`flex items-center px-4 py-2 rounded-2xl ${active === "history" ? "bg-[#0b2b3a] ring-1 ring-[#00E7FF]" : "bg-[#11161b]"}`}
        >
          <FiList className="mr-2" /> Diagnostic History
        </button>
      </div>
    </div>
  );
}
