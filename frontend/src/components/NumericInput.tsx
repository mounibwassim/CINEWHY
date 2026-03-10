import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Minus } from 'lucide-react';

interface NumericInputProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (val: number) => void;
  unit?: string;
}

const NumericInput: React.FC<NumericInputProps> = ({ label, value, min, max, step = 1, onChange, unit = "" }) => {
  const handleIncrement = () => {
    if (value + step <= max) onChange(value + step);
  };

  const handleDecrement = () => {
    if (value - step >= min) onChange(value - step);
  };

  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div className="space-y-4 p-6 glass-card border-white/5 bg-white/[0.02] hover:bg-white/[0.04] transition-colors group">
      <div className="flex justify-between items-end">
        <label className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em]">{label}</label>
        <div className="flex items-center gap-2">
          <AnimatePresence mode="wait">
            <motion.span
              key={value}
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -10, opacity: 0 }}
              className="text-2xl font-poppins font-black text-white"
            >
              {value}
            </motion.span>
          </AnimatePresence>
          {unit && <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">{unit}</span>}
        </div>
      </div>

      <div className="relative h-12 flex items-center gap-4">
        <button
          onClick={handleDecrement}
          className="w-10 h-10 rounded-xl bg-white/5 hover:bg-red-500/20 hover:text-red-400 flex items-center justify-center transition-all border border-white/5 active:scale-90"
        >
          <Minus size={16} />
        </button>

        <div className="flex-1 relative h-2 bg-white/5 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-600 to-blue-400 glow-blue shadow-[0_0_10px_rgba(59,130,246,0.5)]"
          />
          <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
            className="absolute inset-0 w-full opacity-0 cursor-pointer"
          />
        </div>

        <button
          onClick={handleIncrement}
          className="w-10 h-10 rounded-xl bg-white/5 hover:bg-emerald-500/20 hover:text-emerald-400 flex items-center justify-center transition-all border border-white/5 active:scale-90"
        >
          <Plus size={16} />
        </button>
      </div>
    </div>
  );
};

export default NumericInput;
