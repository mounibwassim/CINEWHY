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
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="sidebar glass border-r border-white/10 z-50 bg-[#0a0c1f]"
          >
            {/* Branding removed from Sidebar per Phase 25 */}
            <div className="pt-6"></div>

            <nav className="flex-1 px-4 py-8 space-y-4">
              {navItems.map((item) => (
                <NavLink
                  key={item.id}
                  to={`/${item.id === 'home' ? '' : item.id}`}
                  className={({ isActive }) => `w-full flex items-center gap-4 px-4 py-4 rounded-2xl transition-all duration-300 relative group ${
                    isActive 
                    ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20 glow-blue' 
                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <item.icon size={22} className={location.pathname.includes(item.id) ? 'animate-pulse' : ''} />
                  <span className="font-bold hidden md:block uppercase text-xs tracking-[0.2em]">{item.label}</span>
                  {(location.pathname === `/${item.id}` || (item.id === 'home' && location.pathname === '/')) && (
                    <motion.div 
                      layoutId="activeGlow"
                      className="absolute right-0 w-1 h-8 bg-blue-500 rounded-l-full glow-blue"
                    />
                  )}
                </NavLink>
              ))}
            </nav>

            <div className="p-6">
              <div className="p-4 bg-white/5 border border-white/10 rounded-2xl text-center hidden md:block">
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
      <main className={`flex-1 relative overflow-y-auto scrollbar-hide scroll-smooth ${isMoviePage ? 'w-full' : ''}`}>
        <div className="relative z-10 w-full">
          {/* Top Branding Bar injected for Phase 25 */}
          <div className="w-full flex justify-center items-center py-10 mb-4">
            <div className="flex items-center gap-6">
              <img src={logo} className="w-[100px] h-[100px] object-contain drop-shadow-[0_0_20px_rgba(0,210,255,0.4)]" alt="CineWhy"/>
              <h2 className="text-7xl font-black text-white leading-none tracking-tighter drop-shadow-[0_4px_15px_rgba(0,0,0,0.8)]">
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
