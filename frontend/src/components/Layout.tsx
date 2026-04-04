import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLocation, NavLink } from 'react-router-dom';
import { Home, Filter, BarChart2, Search, Clapperboard, LogOut, Zap, Sparkles, Phone } from 'lucide-react';
import { jwtDecode } from 'jwt-decode';

import logo from '../assets/logo.png';

import Footer from './Footer';

interface LayoutProps {
  children: React.ReactNode;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Layout: React.FC<LayoutProps> = ({ children, activeTab, setActiveTab }) => {
  const location = useLocation();
  const isMoviePage = location.pathname.startsWith('/movie/');
  
  const navItems = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'engine', icon: Filter, label: 'Engine' },
  ];

  // The following function `getPosterUrl` seems to be intended for a different component,
  // likely related to movie data display, as indicated by the instruction "Fix poster logic in AnalyticsDashboard".
  // However, it was provided as an edit within the Layout component's props destructuring.
  // To make the code syntactically correct and incorporate the provided snippet,
  // it's placed here as a standalone function within the Layout component's scope.
  // If this function is truly meant for another component, it should be moved there.
  return (
    <div className="flex h-screen overflow-hidden text-white font-inter bg-[#0f0c29] dashboard">
      {/* Sidebar */}
      <AnimatePresence>
        {!isMoviePage && (
          <motion.aside 
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="sidebar glass z-50 bg-[#0a0c1f] fixed bottom-0 left-0 right-0 border-t border-white/10 md:static md:w-[280px] md:border-t-0 md:border-r md:flex md:flex-col"
          >
            {/* Branding removed from Sidebar per Phase 25 */}
            <div className="pt-6 hidden md:block"></div>

            <nav className="flex flex-row md:flex-col justify-around md:justify-start flex-1 px-4 py-3 md:py-8 md:space-y-4">
              {navItems.map((item) => (
                <NavLink
                  key={item.id}
                  to={`/${item.id === 'home' ? '' : item.id}`}
                  className={({ isActive }) => `flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-4 py-2 md:py-4 rounded-xl md:rounded-2xl transition-all duration-300 relative group md:w-full ${
                    isActive 
                    ? 'text-blue-400 md:bg-blue-500/10 md:border md:border-blue-500/20 md:glow-blue' 
                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <item.icon size={20} className={`md:w-[22px] md:h-[22px] ${location.pathname.includes(item.id) ? 'animate-pulse' : ''}`} />
                  <span className="font-bold text-[9px] md:text-xs tracking-wider md:tracking-[0.2em] md:block uppercase">{item.label}</span>
                  {(location.pathname === `/${item.id}` || (item.id === 'home' && location.pathname === '/')) && (
                    <motion.div 
                      layoutId="activeGlow"
                      className="absolute -top-3 md:top-auto md:right-0 w-8 md:w-1 h-1 md:h-8 bg-blue-500 rounded-b-full md:rounded-l-full glow-blue md:rounded-b-none"
                    />
                  )}
                </NavLink>
              ))}
            </nav>

            <div className="p-6 hidden md:block">
              <div className="p-4 bg-white/5 border border-white/10 rounded-2xl text-center">
                <p className="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">Engine Status</p>
                <div className="flex items-center justify-center gap-2">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
                  <span className="text-xs font-bold text-white tracking-widest uppercase">Operational</span>
                </div>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Content Area */}
      {/* Added mb-20 md:mb-0 padding to prevent content from hiding behind mobile bottom bar */}
      <main className={`flex-1 relative overflow-y-auto scrollbar-hide scroll-smooth mb-[72px] md:mb-0 ${isMoviePage ? 'w-full' : ''}`}>
        <div className="relative z-10 w-full">
          {/* Top Branding Bar injected for Phase 25 */}
          <div className="w-full flex justify-center items-center py-6 md:py-10 mb-2 md:mb-4">
            <div className="flex items-center gap-3 md:gap-6">
              <img src={logo} className="h-[48px] object-contain drop-shadow-[0_0_20px_rgba(0,210,255,0.4)]" alt="CineWhy"/>
              <h2 className="text-4xl md:text-7xl font-black text-white leading-none tracking-tighter drop-shadow-[0_4px_15px_rgba(0,0,0,0.8)]">
                CINE<span className="text-[#1e90ff] drop-shadow-[0_0_20px_rgba(30,144,255,0.6)]">WHY</span>
              </h2>
            </div>
          </div>

          <AnimatePresence mode="popLayout" initial={false}>
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.15 }}
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Footer integration - Only on Welcome Dashboard */}
        {(location.pathname === '/' || location.pathname === '/home') && <Footer />}

        {/* Cinematic Background Accents */}
        <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />
      </main>
    </div>
  );
};

export default Layout;
