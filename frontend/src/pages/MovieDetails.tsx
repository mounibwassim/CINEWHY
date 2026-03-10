import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, Film, Search } from 'lucide-react';

interface MovieDetailsProps {
  movie: any;
  movies?: any[];
  onBack: () => void;
}

const MovieDetails: React.FC<MovieDetailsProps> = ({ movie: movieData, movies, onBack }) => {
  const [imgError, setImgError] = useState(false);
  const posterRef = useRef<HTMLDivElement>(null);
  
  // Handle if movieData is a recommendation { movie, score, fired }
  const movie = movieData?.movie || movieData;
  const explanation = movieData?.fired?.[0]?.explanation || movieData?.explanation;
  const score = movieData?.score || movieData?.inference_score;

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!posterRef.current) return;
    const rect = posterRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (y - centerY) / 8;
    const rotateY = (centerX - x) / 8;
    posterRef.current.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.08, 1.08, 1.08)`;
  };

  const handleMouseLeave = () => {
    if (!posterRef.current) return;
    posterRef.current.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
  };

  if (!movie) {
    return (
      <div className="h-screen flex flex-col items-center justify-center text-center p-12 bg-[#0a0f2f]">
        <Film size={64} className="text-red-500/40 mb-6" />
        <h3 className="text-4xl font-poppins font-black text-white mb-4 uppercase">Movie data unavailable</h3>
        <button onClick={onBack} className="px-10 py-4 bg-blue-600 text-white rounded-2xl font-black uppercase">Return to discovery</button>
      </div>
    );
  }

  const fallbackPoster = "/assets/default-poster.jpg";
  const posterPath = movie.poster_path || movie.poster || movie.posterUrl || movie.image || "";
  const posterUrl = posterPath.startsWith("http")
    ? posterPath
    : (posterPath ? `https://image.tmdb.org/t/p/original${posterPath.startsWith('/') ? posterPath : '/' + posterPath}` : fallbackPoster);

  const currentPoster = !imgError ? posterUrl : fallbackPoster;

  return (
    <div className="movie-details-page-wrapper relative min-h-screen w-full overflow-hidden bg-[#0a0f2f]">
      {/* Blurred immersive background */}
      <div 
        className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat transition-opacity duration-1000 opacity-60"
        style={{ 
          backgroundImage: `url(${currentPoster})`,
          filter: 'blur(80px) brightness(0.6)',
          transform: 'scale(1.2)'
        }}
      />
      
      {/* Dark gradient overlay for readability */}
      <div className="fixed inset-0 z-0 bg-gradient-to-t from-[#0a0f2f] via-[#0a0f2f]/80 to-transparent"></div>
      
      <div className="movie-details-container relative z-10 min-h-screen">
      
      <div className="details-content">
        <motion.button 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          onClick={onBack}
          className="absolute top-0 left-12 flex items-center gap-3 text-slate-400 hover:text-white transition-colors z-50"
        >
          <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center">
            <ArrowLeft size={20} />
          </div>
          <span className="font-black uppercase tracking-[0.3em] text-xs">Return</span>
        </motion.button>

        <div className="flex flex-col md:flex-row items-center gap-16 text-left">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            ref={posterRef}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            className="movie-poster-3d shrink-0 cursor-pointer overflow-hidden rounded-[2rem] transition-transform duration-200 ease-out shadow-[0_50px_100px_rgba(0,0,0,0.8)] border border-white/10"
            style={{ transformStyle: "preserve-3d" }}
          >
             {!imgError ? (
               <img 
                 src={currentPoster} 
                 alt={movie.title} 
                 className="w-full h-full object-cover"
                 style={{ transform: "translateZ(50px)" }}
                 onError={() => setImgError(true)}
               />
             ) : (
               <img 
                 src={fallbackPoster} 
                 alt={movie.title} 
                 className="w-full h-full object-cover"
                 style={{ transform: "translateZ(50px)" }}
               />
             )}
          </motion.div>

          <motion.div 
            initial={{ x: 30, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="space-y-8 flex-1"
          >
            <div className="space-y-2">
              <h1 className="text-6xl md:text-8xl font-poppins font-black text-white leading-tight uppercase tracking-tighter">
                {movie.title}
              </h1>
              <div className="flex flex-wrap items-center gap-6">
                <span className="text-blue-500 font-black text-3xl opacity-80">{movie.year}</span>
                <div className="px-4 py-1.5 bg-yellow-500/20 border border-yellow-500/30 rounded-xl">
                  <span className="text-yellow-400 font-black uppercase text-sm tracking-widest">Rating: {movie.rating || 0}</span>
                </div>
                <div className="px-4 py-1.5 bg-cyan-500/20 border border-cyan-500/30 rounded-xl">
                  <span className="text-cyan-400 font-black uppercase text-sm tracking-widest">{movie.runtime || 0} MIN</span>
                </div>
                {score && (
                  <div className="px-4 py-1.5 bg-blue-500/20 border border-blue-500/30 rounded-xl">
                    <span className="text-blue-400 font-black uppercase text-sm tracking-widest">Match Score: {Math.round(score)}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <label className="text-[10px] font-black text-blue-400 uppercase tracking-[0.3em]">Synoptic Narrative</label>
              <p className="text-xl md:text-2xl text-slate-300 leading-relaxed font-medium">
                {movie.description || "Inference analysis complete. High-fidelity semantic alignment detected for this node in the cinematic web."}
              </p>
            </div>

            {explanation && (
              <div className="space-y-4 p-8 bg-blue-600/10 border border-blue-500/20 rounded-[2rem] backdrop-blur-md">
                <label className="text-[10px] font-black text-blue-400 uppercase tracking-[0.3em]">Cinematic inference (Why Selected)</label>
                <p className="text-blue-200 text-lg italic font-medium">
                  "{explanation}"
                </p>
              </div>
            )}
            
            <div className="flex flex-wrap gap-6 mt-12">
              <a 
                href={`https://www.netflix.com/search?q=${encodeURIComponent(movie.title)}`} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="btn-netflix-cine flex items-center gap-3 px-8 py-4 bg-[#e50914] hover:bg-[#ff0f1a] text-white rounded-2xl font-black uppercase tracking-widest transition-all shadow-[0_10px_30px_rgba(229,9,20,0.4)] hover:scale-105 active:scale-95"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 1.5c-1.104 0-2 .896-2 2v10.5h-2v-12.5c0-1.104-.896-2-2-2h-2c-1.104 0-2 .896-2 2v12.5h-2v-10.5c0-1.104-.896-2-2-2h-2c-1.104 0-2 .896-2 2v19h4v-11h2v11h4v-11h2v11h4v-19c0-1.104-.896-2-2-2h-2z" style={{display: 'none'}} />
                  {/* Better Netflix 'N' Path */}
                  <path d="M4 2v20h4V3.6l8 16.8V22h4V2l-4 0v18.4L8 2z"/>
                </svg>
                Watch on Netflix
              </a>
              <a 
                href={`https://www.google.com/search?q=${encodeURIComponent(movie.title + " movie")}`} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="btn-google-cine flex items-center gap-3 px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-2xl font-black uppercase tracking-widest transition-all hover:scale-105 active:scale-95"
              >
                <Search size={20} />
                Discover More
              </a>
            </div>
          </motion.div>
        </div>
      </div>
      </div>
    </div>
  );
};

export default MovieDetails;
