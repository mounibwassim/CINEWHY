import React, { useState, useEffect, Suspense, lazy } from 'react';
import { Routes, Route, useNavigate, useLocation, Navigate, useParams } from 'react-router-dom';
import Layout from './components/Layout';

const WelcomeDashboard = lazy(() => import('./pages/WelcomeDashboard'));
const MainDashboard = lazy(() => import('./pages/MainDashboard'));
const ResultsDashboard = lazy(() => import('./pages/ResultsDashboard'));
const MovieDetails = lazy(() => import('./pages/MovieDetails'));
const InfoPage = lazy(() => import('./pages/InfoPage'));

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

interface Movie {
  id: number;
  title: string;
  year: number;
  genres: string[];
  rating: number;
  votes: number;
  runtime: number;
  quality: string;
  pop_band: string;
  runtime_cat: string;
  description?: string;
  poster_url?: string;
  poster_path?: string;
  popularity?: number;
}

interface Recommendation {
  movie: Movie;
  score: number;
  fired: {
    rule_id: string;
    description: string;
    explanation: string;
  }[];
}

interface InitData {
  movies: Movie[];
  genres: string[];
  year_min: number;
  year_max: number;
  pop_options: string[];
  runtime_options: string[];
}

const App: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [initData, setInitData] = useState<InitData | null>(null);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [incGenres, setIncGenres] = useState<string[]>([]);
  const [excGenres, setExcGenres] = useState<string[]>([]);
  const [yearFrom, setYearFrom] = useState<number>(1900);
  const [yearTo, setYearTo] = useState<number>(2024);
  const [minRating, setMinRating] = useState<number>(0);
  const [popPref, setPopPref] = useState<string>('any');
  const [runtimePref, setRuntimePref] = useState<string>('any');
  const [topK, setTopK] = useState<number>(10);
  
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [initError, setInitError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Wrapper component to get movie from location.state or from initData via ID
  const MovieDetailsWrapper: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const movieData = location.state?.movie || initData?.movies.find(m => m.id === Number(id)) || selectedMovie;
    
    // Safety check: if movieData is missing, show error state
    if (!movieData) {
      return (
        <div className="h-[80vh] flex flex-col items-center justify-center text-center p-12 bg-[#0a0f2f]">
          <h3 className="text-3xl font-poppins font-black text-white mb-4 uppercase tracking-tight">Movie Data Offline</h3>
          <p className="text-slate-500 max-w-md font-medium leading-relaxed">The requested cinematic data could not be retrieved from the current operational node.</p>
          <button 
            onClick={() => navigate('/engine')}
            className="mt-6 px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-black uppercase tracking-widest transition-all shadow-lg"
          >
            Return to discovery
          </button>
        </div>
      );
    }
    
    return <MovieDetails movie={movieData} movies={initData?.movies} onBack={() => navigate(-1)} />;
  };

  useEffect(() => {
    localStorage.setItem('cine_recs', JSON.stringify(recommendations));
  }, [recommendations]);

  useEffect(() => {
    const fetchInit = async (attempt = 0) => {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000); // 15s timeout
        const res = await fetch(`${API_BASE_URL}/api/init`, { signal: controller.signal });
        clearTimeout(timeout);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: InitData = await res.json();
        setInitData(data);
        setYearFrom(data.year_min);
        setYearTo(data.year_max);
        setInitError(null);
      } catch (err: any) {
        console.error('Error fetching init data:', err);
        if (attempt < 3) {
          setRetryCount(attempt + 1);
          setTimeout(() => fetchInit(attempt + 1), 2000);
        } else {
          setInitError(`Could not connect to backend at ${API_BASE_URL}. Check that the server is running and CORS is enabled.`);
        }
      }
    };
    fetchInit();
  }, []);

  const getRecommendations = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/api/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        inc_genres: incGenres,
        exc_genres: excGenres,
        year_from: yearFrom,
        year_to: yearTo,
        min_rating: minRating,
        pop_pref: popPref,
        runtime_pref: runtimePref,
        top_k: topK
      })
    })
      .then(res => res.json())
      .then(data => {
        // Enrich recommendations with posters from initData if missing
        const enrichedResults = data.results.map((rec: any) => {
          let movie = rec.movie;
          if (!movie.poster_path && initData) {
            const match = initData.movies.find(m => m.id === movie.id);
            if (match) movie.poster_path = match.poster_path;
          }
          // Ensure poster_path has leading slash if it exists
          if (movie.poster_path && !movie.poster_path.startsWith('/')) {
            movie.poster_path = `/${movie.poster_path}`;
          }
          return rec;
        });
        setRecommendations(enrichedResults);
        setLoading(false);
        navigate('/results'); 
      })
      .catch(err => {
        console.error('Error fetching recommendations:', err);
        setLoading(false);
      });
  };

  const toggleGenre = (genre: string, type: 'inc' | 'exc') => {
    if (type === 'inc') {
      setIncGenres(prev => prev.includes(genre) ? prev.filter(g => g !== genre) : [...prev, genre]);
      // Ensure excluded genres do not overlap
      setExcGenres(prev => prev.filter(g => g !== genre));
    } else {
      setExcGenres(prev => prev.includes(genre) ? prev.filter(g => g !== genre) : [...prev, genre]);
      // Ensure included genres do not overlap
      setIncGenres(prev => prev.filter(g => g !== genre));
    }
  };

  const handleMovieClick = (data: any, posterUrl?: string | null) => {
    const movie = data.movie || data;
    if (posterUrl) {
      movie.poster = posterUrl;
    }
    const payload = data.movie ? { ...data, movie } : movie;
    setSelectedMovie(payload);
    // Navigate strictly passing the enriched movie payload
    navigate(`/movie/${movie.id}`, { 
      state: { movie: payload } 
    });
  };

  if (initError) return (
    <div className="h-screen bg-[#0a0f2f] flex flex-col items-center justify-center gap-8 p-8 text-center">
      <div className="text-6xl">🎬</div>
      <h2 className="font-poppins font-black text-white text-2xl uppercase tracking-widest">Backend Offline</h2>
      <p className="text-slate-400 max-w-md">{initError}</p>
      <button
        onClick={() => { setInitError(null); setRetryCount(0); }}
        className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-black uppercase tracking-widest transition-all"
      >
        Retry Connection
      </button>
    </div>
  );

  if (!initData) return (
    <div className="h-screen bg-[#0a0f2f] flex flex-col items-center justify-center gap-8">
      <div className="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
      <span className="font-poppins font-black text-blue-500 tracking-[0.5em] animate-pulse">BOOTING ENGINE...</span>
      {retryCount > 0 && (
        <span className="text-slate-500 text-sm">Connecting to backend... attempt {retryCount}/3</span>
      )}
      <span className="text-slate-600 text-xs mt-2">{API_BASE_URL}</span>
    </div>
  );

  const currentPath = location.pathname;
  let activeTab = 'home';
  if (currentPath.startsWith('/home')) activeTab = 'home';
  else if (currentPath.startsWith('/engine') || currentPath.startsWith('/results') || currentPath.startsWith('/movie')) activeTab = 'engine';
  else if (currentPath.startsWith('/info')) activeTab = 'home';

  const handleTabChange = (tab: string) => {
    console.log(`App: Switching to ${tab}`);
    navigate(`/${tab}`);
  };

  return (
    <Layout 
      activeTab={activeTab} 
      setActiveTab={handleTabChange}
    >
        <Suspense fallback={
          <div className="loading-screen">Loading CineWhy...</div>
        }>
          <Routes>
            <Route path="/" element={<WelcomeDashboard onStart={() => navigate('/engine')} />} />
            <Route path="/home" element={<Navigate to="/" replace />} />
            <Route path="/engine" element={
              <MainDashboard 
                initData={initData}
                incGenres={incGenres}
                excGenres={excGenres}
                yearFrom={yearFrom}
                yearTo={yearTo}
                minRating={minRating}
                popPref={popPref}
                runtimePref={runtimePref}
                topK={topK}
                loading={loading}
                setYearFrom={setYearFrom}
                setYearTo={setYearTo}
                setMinRating={setMinRating}
                setPopPref={setPopPref}
                setRuntimePref={setRuntimePref}
                setTopK={setTopK}
                toggleGenre={toggleGenre}
                getRecommendations={getRecommendations}
                onMovieClick={handleMovieClick}
              />
            } />
            <Route path="/results" element={<ResultsDashboard recommendations={recommendations} onMovieClick={handleMovieClick} />} />
            <Route path="/info/:type" element={<InfoPage />} />
            <Route path="/movie/:id" element={<MovieDetailsWrapper />} />
            <Route path="/movie-details" element={<Navigate to={`/movie/${selectedMovie?.id || ''}`} replace />} />
            <Route path="/movie" element={<Navigate to="/engine" replace />} />
            {/* Legacy route cleanup */}
            <Route path="/main" element={<Navigate to="/engine" replace />} />
            <Route path="/analytics" element={<Navigate to="/insights" replace />} />
            <Route path="/details" element={<Navigate to="/engine" replace />} />
          </Routes>
        </Suspense>
      </Layout>
  );
};

export default App;
