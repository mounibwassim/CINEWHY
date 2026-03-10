import React, { useRef } from 'react';
import { motion } from 'framer-motion';
import { Filter, Sparkles } from 'lucide-react';
import NumericInput from '../components/NumericInput';

interface MainDashboardProps {
  initData: any;
  incGenres: string[];
  excGenres: string[];
  yearFrom: number;
  yearTo: number;
  minRating: number;
  popPref: string;
  runtimePref: string;
  topK: number;
  loading: boolean;
  setYearFrom: (val: number) => void;
  setYearTo: (val: number) => void;
  setMinRating: (val: number) => void;
  setPopPref: (val: string) => void;
  setRuntimePref: (val: string) => void;
  setTopK: (val: number) => void;
  toggleGenre: (genre: string, type: 'inc' | 'exc') => void;
  getRecommendations: () => void;
  onMovieClick: (movie: any, posterUrl?: string | null) => void;
}

const MainDashboard: React.FC<MainDashboardProps> = (props) => {
  const { 
    initData, incGenres, excGenres, yearFrom, yearTo, minRating, 
    popPref, runtimePref, topK, loading, 
    setYearFrom, setYearTo, setMinRating, setPopPref, setRuntimePref, setTopK,
    toggleGenre, getRecommendations
  } = props;

  if (!initData) {
    return (
      <div className="h-[80vh] flex flex-col items-center justify-center text-center p-12">
        <Sparkles size={64} className="text-blue-500/20 mb-6" />
        <h3 className="text-3xl font-poppins font-black text-white mb-4 uppercase">Discovery Engine Offline</h3>
      </div>
    );
  }

  return (
    <div className="relative w-full overflow-hidden">
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="p-8 max-w-6xl mx-auto space-y-12 relative z-10"
      >

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
          <section className="glass-card space-y-8 relative overflow-hidden group border-white/5 bg-white/[0.01]">
            <div className="flex items-center gap-3 border-b border-white/5 pb-4">
              <Filter className="text-blue-400" size={24} />
              <h3 className="font-poppins font-black text-2xl tracking-tighter uppercase">Genre Architecture</h3>
            </div>
            <div className="space-y-10">
              <div>
                <label className="block text-[10px] font-black text-blue-400 uppercase tracking-[0.3em] mb-6">Required</label>
                <div className="flex flex-wrap gap-3">
                  {initData.genres.map((g: string) => (
                    <button key={g} onClick={() => toggleGenre(g, 'inc')} className={`chip-3d px-5 py-2.5 rounded-2xl text-xs font-black uppercase tracking-widest transition-all ${incGenres.includes(g) ? 'chip-3d-active' : 'hover:bg-white/5'}`}>{g}</button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-[10px] font-black text-red-400 uppercase tracking-[0.3em] mb-6">Exclude</label>
                <div className="flex flex-wrap gap-3">
                  {initData.genres.map((g: string) => (
                    <button key={g} onClick={() => toggleGenre(g, 'exc')} className={`chip-3d px-5 py-2.5 rounded-2xl text-xs font-black uppercase tracking-widest transition-all ${excGenres.includes(g) ? 'chip-3d-exclude' : 'hover:bg-white/5'}`}>{g}</button>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <NumericInput label="From" value={yearFrom} min={initData.year_min} max={yearTo} onChange={setYearFrom} unit="Year" />
              <NumericInput label="To" value={yearTo} min={yearFrom} max={initData.year_max} onChange={setYearTo} unit="Year" />
            </div>
            <NumericInput label="Rating" value={minRating} min={0} max={10} step={0.1} onChange={setMinRating} unit="Score" />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4 p-6 glass-card border-white/5 bg-white/[0.02]">
                <label className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em]">Popularity</label>
                <select value={popPref} onChange={e => setPopPref(e.target.value)} className="w-full bg-white/5 border border-white/5 rounded-2xl px-5 py-4 text-white font-bold outline-none">
                  {initData.pop_options.map((opt: string) => <option key={opt} value={opt} className="bg-[#0f0c29]">{opt.toUpperCase()}</option>)}
                </select>
              </div>
              <div className="space-y-4 p-6 glass-card border-white/5 bg-white/[0.02]">
                <label className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em]">Runtime</label>
                <select value={runtimePref} onChange={e => setRuntimePref(e.target.value)} className="w-full bg-white/5 border border-white/5 rounded-2xl px-5 py-4 text-white font-bold outline-none">
                  {initData.runtime_options.map((opt: string) => <option key={opt} value={opt} className="bg-[#0f0c29]">{opt.toUpperCase()}</option>)}
                </select>
              </div>
            </div>
            <NumericInput label="Matches" value={topK} min={1} max={100} onChange={setTopK} unit="Count" />
          </div>
        </div>

        <div className="flex justify-center pt-8">
          <motion.button onClick={getRecommendations} disabled={loading} className="btn-premium text-2xl font-black px-24 py-8 relative overflow-hidden group shadow-2xl tracking-widest uppercase">
            <div className="absolute inset-0 bg-blue-600 group-hover:bg-blue-500 transition-all" />
            <span className="relative z-10">{loading ? 'Calibrating...' : 'Initialize Discovery'}</span>
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
};

export default MainDashboard;
