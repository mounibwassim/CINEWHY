import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Star, Info, Award, TrendingUp, Sparkles, Trophy, Zap, Film, Globe, PlayCircle } from 'lucide-react';
import { deduplicateMovies } from '../utils';

// ─── INTERACTIVE MOVIE CARD ────────────────────────────────────────────────────
interface InteractiveMovieCardProps {
  movieRec: any;
  onClick: (movie: any, url: string) => void;
}

const InteractiveMovieCard = ({ movieRec, onClick }: InteractiveMovieCardProps) => {
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    const rotX = ((y - cy) / cy) * -15; // Increased tilt
    const rotY = ((x - cx) / cx) * 15;
    cardRef.current.style.transform = `perspective(1000px) scale(1.08) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-5px)`;
    cardRef.current.style.boxShadow = `0 20px 40px rgba(109, 40, 217, 0.4), ${(x - cx) * 0.15}px ${(y - cy) * 0.15}px 30px rgba(59,130,246,0.3)`;
    
    // Move the glow effect smoothly
    const overlay = cardRef.current.querySelector('.shine-overlay') as HTMLDivElement;
    if (overlay) {
      overlay.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 60%)`;
    }
  };

  const handleMouseLeave = () => {
    if (!cardRef.current) return;
    cardRef.current.style.transform = 'perspective(1000px) scale(1) rotateX(0deg) rotateY(0deg) translateY(0)';
    cardRef.current.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
    const overlay = cardRef.current.querySelector('.shine-overlay') as HTMLDivElement;
    if (overlay) {
      overlay.style.background = 'none';
    }
  };

  const movie = movieRec.movie || movieRec;

  // Force 4K TMDB poster & premium 3D clapperboard fallback
  const raw = movie.poster_path || movie.poster || movie.posterUrl || movie.image || '';
  const fallbackPoster = '/assets/default-poster.jpg';
  const posterUrl = raw.startsWith('http')
    ? raw
    : raw
      ? `https://image.tmdb.org/t/p/original${raw.startsWith('/') ? raw : '/' + raw}`
      : fallbackPoster;

  // Generate a visually deterministic cinematic gradient background
  const colors = [
    'linear-gradient(145deg, #1e1b4b 0%, #312e81 100%)', // Deep Indigo
    'linear-gradient(145deg, #31102a 0%, #701a34 100%)', // Crimson Dark
    'linear-gradient(145deg, #14332b 0%, #064e3b 100%)', // Emerald Dark
    'linear-gradient(145deg, #322510 0%, #78350f 100%)', // Amber Dark
    'linear-gradient(145deg, #0f172a 0%, #1e293b 100%)', // Slate Slate
    'linear-gradient(145deg, #2e1065 0%, #4c1d95 100%)', // Violet Dark
  ];
  const colorIndex = (movie.title.length + (movie.id || 0)) % colors.length;
  const cardGradient = colors[colorIndex];

  return (
    <div
      ref={cardRef}
      className="movie-card relative flex flex-col items-center cursor-pointer rounded-2xl overflow-hidden border border-white/10"
      style={{ 
        background: cardGradient,
        transition: 'transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)', 
        transformStyle: 'preserve-3d',
        boxShadow: '0 10px 30px rgba(0,0,0,0.5)'
      }}
      onClick={() => onClick(movieRec, posterUrl)}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      <div className="shine-overlay absolute inset-0 z-10 pointer-events-none rounded-2xl transition-all duration-75"></div>
      
      <div className="w-full relative pt-2 px-2">
        <img
          src={posterUrl}
          alt={movie.title}
          className="w-full h-[320px] object-cover rounded-xl shadow-[0_8px_16px_rgba(0,0,0,0.6)]"
          loading="lazy"
          onError={(e) => {
            e.currentTarget.src = fallbackPoster;
          }}
        />
        {/* Rating badge */}
        <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 flex items-center gap-1.5 shadow-lg">
          <Star size={12} className="text-yellow-400 fill-yellow-400" />
          <span className="text-white text-xs font-bold">{movie.rating || 'N/A'}</span>
        </div>
      </div>

      <div className="w-full p-4 flex flex-col items-center justify-center flex-grow bg-gradient-to-t from-black/60 to-transparent">
        <h3 className="text-white font-black text-center text-lg leading-tight drop-shadow-md mb-2 line-clamp-2">
          {movie.title}
        </h3>
        <div className="flex gap-2 items-center opacity-80">
          <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-white/10 text-white/90 border border-white/5 uppercase tracking-wide">
            {movie.year || '----'}
          </span>
          <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-blue-500/20 text-blue-300 border border-blue-500/20 uppercase tracking-wide flex items-center gap-1">
            <Film size={10} />
            {movie.genres?.[0] || 'Movie'}
          </span>
        </div>
      </div>

      <div className="card-overlay flex flex-col justify-center items-center bg-black/80 backdrop-blur-sm z-20">
        <PlayCircle size={48} className="text-pink-500 mb-3 drop-shadow-[0_0_15px_rgba(236,72,153,0.8)]" />
        <div className="view-details-btn text-white font-black text-xl tracking-widest uppercase flex items-center gap-2">
          View Details
        </div>
      </div>
    </div>
  );
};


// ─── 3D STAT CARD ──────────────────────────────────────────────────────────────
interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub?: string;
  gradient: string;
  glow: string;
  iconBg: string;
}

const StatCard = ({ icon, label, value, sub, gradient, glow, iconBg }: StatCardProps) => {
  const ref = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    const rotX = ((y - cy) / cy) * -10;
    const rotY = ((x - cx) / cx) * 10;
    ref.current.style.transform = `perspective(800px) scale(1.07) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    ref.current.style.boxShadow = `0 20px 60px ${glow}`;
  };

  const handleMouseLeave = () => {
    if (!ref.current) return;
    ref.current.style.transform = 'perspective(800px) scale(1) rotateX(0deg) rotateY(0deg)';
    ref.current.style.boxShadow = `0 8px 30px ${glow}55`;
  };

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        background: gradient,
        boxShadow: `0 8px 30px ${glow}55`,
        transition: 'transform 0.18s ease, box-shadow 0.18s ease',
        transformStyle: 'preserve-3d',
      }}
      className="relative overflow-hidden rounded-3xl p-6 flex flex-col gap-3 select-none cursor-default border border-white/10"
    >
      {/* Glow orb background */}
      <div
        className="absolute -top-6 -right-6 w-28 h-28 rounded-full opacity-30 blur-2xl"
        style={{ background: glow }}
      />
      {/* Icon */}
      <div
        className="w-12 h-12 rounded-2xl flex items-center justify-center text-white shadow-lg"
        style={{ background: iconBg }}
      >
        {icon}
      </div>
      {/* Label */}
      <span className="text-white/60 text-[10px] font-black uppercase tracking-[0.25em]">{label}</span>
      {/* Value */}
      <div className="flex items-end gap-2">
        <span className="text-3xl font-black text-white leading-none">{value}</span>
        {sub && <span className="text-white/40 text-sm font-bold mb-0.5">{sub}</span>}
      </div>
    </motion.div>
  );
};

// ─── RESULTS DASHBOARD ─────────────────────────────────────────────────────────
interface ResultsDashboardProps {
  recommendations: any[];
  onMovieClick: (movie: any, posterUrl?: string | null) => void;
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ recommendations, onMovieClick }) => {
  console.log('Results Dashboard Input:', recommendations);

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="h-[80vh] flex flex-col items-center justify-center text-center p-12 bg-[#0a0f2f] dashboard-page">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="p-8 bg-blue-500/5 rounded-[3rem] border border-blue-500/10 mb-8"
        >
          <Sparkles size={64} className="text-blue-500/40" />
        </motion.div>
        <h3 className="text-3xl font-poppins font-black text-white mb-4 uppercase tracking-tight">Discovery Queue Empty</h3>
        <p className="text-slate-500 max-w-md font-medium leading-relaxed mb-8">
          Adjust your filtering parameters in the Engine dashboard to generate new high-fidelity recommendations.
        </p>
        <button
          onClick={() => window.location.href = '/engine'}
          className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-black uppercase tracking-widest transition-all shadow-lg"
        >
          Go to Engine
        </button>
      </div>
    );
  }

  const uniqueRecs = deduplicateMovies(recommendations);
  const sortedRecs = [...uniqueRecs].sort((a, b) => b.score - a.score);

  const avgScore = sortedRecs.length > 0
    ? (sortedRecs.reduce((acc, r) => acc + r.score, 0) / sortedRecs.length).toFixed(1)
    : '0';

  const avgRating = sortedRecs.length > 0
    ? (sortedRecs.reduce((acc, r) => {
        const m = r.movie || r;
        return acc + (m.rating || 0);
      }, 0) / sortedRecs.length).toFixed(1)
    : '0';

  const allGenres = sortedRecs.flatMap(r => {
    const m = r.movie || r;
    return m.genres || [];
  });
  const genreCounts = allGenres.reduce((acc: Record<string, number>, g) => {
    acc[g] = (acc[g] || 0) + 1;
    return acc;
  }, {});
  const topGenreEntry = Object.entries(genreCounts).sort((a, b) => b[1] - a[1])[0];
  const topGenre = topGenreEntry ? topGenreEntry[0] : 'N/A';
  const topGenreVal = topGenreEntry ? topGenreEntry[1] : 0;

  const statCards: StatCardProps[] = [
    {
      icon: <Star size={22} />,
      label: 'Avg Match Rating',
      value: `${avgRating}`,
      sub: '/ 10',
      gradient: 'linear-gradient(135deg, #1a1040 0%, #2d1b6e 100%)',
      glow: '#7c3aed',
      iconBg: 'linear-gradient(135deg, #7c3aed, #a855f7)',
    },
    {
      icon: <Zap size={22} />,
      label: 'Avg Inference',
      value: `${avgScore}`,
      sub: 'pts',
      gradient: 'linear-gradient(135deg, #0c1a40 0%, #1a3a7a 100%)',
      glow: '#3b82f6',
      iconBg: 'linear-gradient(135deg, #2563eb, #3b82f6)',
    },
    {
      icon: <Film size={22} />,
      label: 'Top Genre',
      value: topGenre,
      sub: `(top ${topGenreVal})`,
      gradient: 'linear-gradient(135deg, #0c2a1c 0%, #1a4a2c 100%)',
      glow: '#10b981',
      iconBg: 'linear-gradient(135deg, #059669, #10b981)',
    },
    {
      icon: <Globe size={22} />,
      label: 'Dataset Reach',
      value: '2,000+',
      sub: 'movies',
      gradient: 'linear-gradient(135deg, #2a0c1a 0%, #4a1a2e 100%)',
      glow: '#f43f5e',
      iconBg: 'linear-gradient(135deg, #e11d48, #f43f5e)',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8 max-w-[1400px] mx-auto pb-32 dashboard-page"
    >
      {/* Header */}
      <div className="pt-8 mb-10 flex items-center gap-4 border-b border-white/5 pb-6">
        <Trophy className="text-yellow-500" size={32} />
        <div>
          <h2 className="text-4xl font-poppins font-black text-white uppercase tracking-tight">Discovery Results</h2>
          <p className="text-slate-400 mt-2 font-medium">Movies matching your preferences — hover the cards to interact</p>
        </div>
      </div>

      {/* ── Premium 3D Stat Cards ── */}
      <section className="mb-14">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {statCards.map((card, i) => (
            <StatCard key={i} {...card} />
          ))}
        </div>
      </section>

      {/* ── Movie Grid ── */}
      <section className="mb-20">
        {sortedRecs && sortedRecs.length > 0 ? (
          <div className="results-movie-grid">
            {sortedRecs.map((movieRec, index) => {
              const movie = movieRec.movie || movieRec;
              return (
                <InteractiveMovieCard
                  key={movie.id || index}
                  movieRec={movieRec}
                  onClick={onMovieClick}
                />
              );
            })}
          </div>
        ) : (
          <div className="results-empty flex justify-center items-center py-20 bg-black/20 rounded-2xl border border-white/5">
            <span className="text-xl font-bold text-slate-400">No movies found. Try adjusting your discovery settings.</span>
          </div>
        )}
      </section>

      {/* ── Why CineWhy ── */}
      <section className="why-cinewhy text-center max-w-4xl mx-auto flex flex-col items-center">
        <h2 className="text-3xl font-poppins font-black text-white mb-6 drop-shadow-md">Why Use CineWhy</h2>
        <p className="text-slate-300 text-lg mb-8 leading-relaxed">
          CineWhy predicts movies with 95% semantic accuracy using an advanced discovery engine.
        </p>
        <div className="flex flex-col md:flex-row justify-center gap-6 md:gap-12 text-left bg-[#161930]/40 p-8 rounded-2xl border border-white/5 w-full">
          {['Over 2,000+ movies analyzed', 'Smart semantic inference scoring', 'AI-powered recommendation intelligence'].map((txt, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_#3b82f6]" />
              <span className="text-white font-medium">{txt}</span>
            </div>
          ))}
        </div>
      </section>
    </motion.div>
  );
};

export default ResultsDashboard;
