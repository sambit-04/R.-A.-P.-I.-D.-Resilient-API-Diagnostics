import React from "react";
import { motion } from "framer-motion";

export default function ProgressModal({ open, progress=0, onCancel }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onCancel}></div>
      <motion.div initial={{y:40, opacity:100}} animate={{y:0, opacity:1}} className="relative bg-card rounded-2xl p-6 w-11/12 max-w-md">
        <h3 className="text-lg font-semibold text-[#00E7FF]">Test Running</h3>
        <p className="text-sm text-[#8B949E] mt-2">Progress: {progress}%</p>
        <div className="mt-4 bg-[#0b1220] rounded-full h-4 overflow-hidden border border-[#263038]">
          <div style={{ width: `${progress}%`}} className="h-4 rounded-full" />
        </div>

        <div className="mt-6 flex justify-end space-x-3">
          <button onClick={onCancel} className="px-4 py-2 rounded-2xl bg-[#111418] border border-[#263038]">Cancel</button>
        </div>
      </motion.div>
    </div>
  );
}
