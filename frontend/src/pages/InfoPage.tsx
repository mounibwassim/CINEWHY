import React from 'react';
import { motion } from 'framer-motion';
import { Info, Mail, Phone, Shield, FileText, Users, MessageSquare, Trophy, LifeBuoy, ArrowLeft } from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';

const InfoPage: React.FC = () => {
  const { type } = useParams<{ type: string }>();
  const navigate = useNavigate();

  const contentMap: Record<string, any> = {
    'tmdb': {
      title: 'About TMDB',
      icon: Info,
      text: 'CineWhy utilizes the TMDB API for movie data and posters. We are not endorsed or certified by TMDB.',
      details: 'Our application relies on the comprehensive database provided by The Movie Database (TMDB) to bring you the latest information on over 2,000+ cinematic titles. This integration allows us to provide high-resolution posters, accurate ratings, and detailed metadata.'
    },
    'contact-us': {
      title: 'Contact Us',
      icon: Mail,
      text: 'Reach out to the CineWhy development team.',
      details: (
        <div className="space-y-4">
          <p>You can reach us directly via the following channels:</p>
          <div className="flex flex-col gap-6 pt-4">
            <a href="mailto:mounibwassimm@gmail.com" className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 hover:border-blue-500/50 hover:bg-blue-500/5 transition-all group">
               <Mail className="text-blue-400 group-hover:scale-110 transition-transform" size={24} />
               <div className="flex flex-col">
                 <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Email Address</span>
                 <span className="text-lg font-black text-white">mounibwassimm@gmail.com</span>
               </div>
            </a>
            <a href="https://wa.me/601111769636" target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 hover:border-emerald-500/50 hover:bg-emerald-500/5 transition-all group">
               <Phone className="text-emerald-400 group-hover:scale-110 transition-transform" size={24} />
               <div className="flex flex-col">
                 <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">WhatsApp Support</span>
                 <span className="text-lg font-black text-white group-hover:text-emerald-400 transition-colors">+60 01111769636</span>
               </div>
            </a>
          </div>
        </div>
      )
    },
    'privacy': {
      title: 'Privacy Policy',
      icon: Shield,
      text: 'Your data security is our priority.',
      details: 'CineWhy does not store your personal browsing history. We use local storage for your preferences and secure Google OAuth for authentication. Your discovery patterns are processed in real-time and are not sold to third parties.'
    },
    'terms': {
      title: 'Terms of Service',
      icon: FileText,
      text: 'Platform usage guidelines.',
      details: 'By using CineWhy, you agree to our fair use policy. The recommendation engine is provided "as is" for entertainment and discovery purposes. All dataset rights belong to their respective creators.'
    },
    'guidelines': {
      title: 'Community Guidelines',
      icon: Users,
      text: 'Keeping discovery respectful.',
      details: 'We encourage sharing your discoveries! Our community thrives on unique perspectives. Please maintain a professional tone in discussions and respect the diverse cinematic tastes of all members.'
    },
    'discussions': {
      title: 'Discussions',
      icon: MessageSquare,
      text: 'Connect with other movie enthusiasts.',
      details: 'Join our weekly cinematic breakdown where we discuss high-fidelity match hits and hidden gems found using the CineWhy engine.'
    },
    'leaderboard': {
      title: 'Leaderboard',
      icon: Trophy,
      text: 'Top discovery engines this month.',
      details: 'See who has found the rarest cinematic patterns. Our leaderboard tracks the most unique filtering combinations that yielded high-quality results.'
    },
    'support': {
      title: 'Support Forums',
      icon: LifeBuoy,
      text: 'Get help with the discovery architecture.',
      details: 'Experiencing lag in inference? Or posters not loading? Our community support forums are active 24/7 to help you calibrate your local engine.'
    }
  };

  const currentContent = contentMap[type || ''] || contentMap['tmdb'];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-12 max-w-4xl mx-auto space-y-12 pb-32"
    >
      <button 
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-slate-500 hover:text-white transition-colors group"
      >
        <ArrowLeft size={18} className="group-hover:-translate-x-1 transition-transform" />
        <span className="text-[10px] font-black uppercase tracking-widest">Back</span>
      </button>

      <div className="space-y-8">
        <div className="flex items-center gap-6">
          <div className="p-4 bg-blue-500/10 rounded-[2rem] border border-blue-500/20 glow-blue">
            <currentContent.icon size={48} className="text-blue-400" />
          </div>
          <div>
            <h1 className="text-5xl md:text-6xl font-poppins font-black text-white leading-none uppercase tracking-tight">
              {currentContent.title}
            </h1>
            <p className="text-blue-500 font-bold uppercase tracking-[0.3em] text-[10px] mt-2">{currentContent.text}</p>
          </div>
        </div>

        <div className="glass-card p-12 border-white/5 bg-white/[0.01] relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px] -mr-32 -mt-32" />
          <div className="text-xl text-slate-400 leading-relaxed font-medium whitespace-pre-wrap relative z-10">
            {currentContent.details}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default InfoPage;
