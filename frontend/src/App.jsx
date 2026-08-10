import React, { useState } from "react";
import Navbar from "./components/Navbar";
import DiagnosticTool from "./components/DiagnosticTool";
import DiagnosticHistory from "./components/DiagnosticHistory";

export default function App() {
  const [tab, setTab] = useState("tool");

  return (
    <div className="min-h-screen text-[#E6EDF3]">
      <div className="max-w-6xl mx-auto p-6">
        <Navbar active={tab} onChange={setTab} />
        <main className="mt-6">
          {tab === "tool" ? <DiagnosticTool /> : <DiagnosticHistory />}
        </main>
      </div>
    </div>
  );
}
