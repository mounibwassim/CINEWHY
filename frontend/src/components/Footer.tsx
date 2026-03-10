import React from 'react';
import { motion } from 'framer-motion';
import { Mail, Phone, Instagram, Github, Share2 } from 'lucide-react';
import { Link } from 'react-router-dom';

const XIcon = ({ size, className }: { size: number, className?: string }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" className={className}>
    <path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932 6.064-6.932zm-1.292 19.494h2.039L6.486 3.24H4.298l13.311 17.407z" />
  </svg>
);

const Footer: React.FC = () => {
  const sections = [
    {
      title: "The Basics",
      links: [
        { label: "About TMDB", path: "/info/tmdb" },
        { label: "Contact Us", path: "/info/contact-us" },
        { label: "Privacy Policy", path: "/info/privacy" },
        { label: "Terms of Service", path: "/info/terms" }
      ]
    },
    {
      title: "Community",
      links: [
        { label: "Guidelines", path: "/info/guidelines" },
        { label: "Discussions", path: "/info/discussions" },
        { label: "Leaderboard", path: "/info/leaderboard" },
        { label: "Support Forums", path: "/info/support" }
      ]
    }
  ];

  const socialLinks = [
    { icon: Instagram, url: "https://www.instagram.com/accounts/login/", color: "hover:text-pink-500" },
    { icon: XIcon, url: "https://x.com/login", color: "hover:text-white" },
    { icon: Github, url: "https://github.com/login", color: "hover:text-white" }
  ];

  return (
    <footer className="relative mt-20 border-t border-white/5 bg-[#0a0c1f]/80 backdrop-blur-xl py-20 overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
      
      <div className="max-w-7xl mx-auto px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8">
          {/* Logo & Vision */}
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-500/20">
                <Share2 size={24} className="text-white" />
              </div>
              <span className="font-poppins font-black text-2xl tracking-tighter text-white">CINE<span className="text-blue-500">WHY</span></span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed font-medium">
              Redefining cinematic discovery through advanced inference architecture and high-fidelity dataset analysis.
            </p>
            <div className="flex gap-4">
              {socialLinks.map((social, i) => (
                <motion.a 
                  key={i}
                  href={social.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1, y: -2 }}
                  className={`p-2.5 bg-white/5 rounded-xl border border-white/10 text-slate-400 transition-colors ${social.color}`}
                >
                  <social.icon size={20} />
                </motion.a>
              ))}
            </div>
          </div>

          {/* Dynamic Sections */}
          {sections.map((section, idx) => (
            <div key={idx} className="space-y-6">
              <h4 className="text-xs font-black uppercase tracking-[0.3em] text-blue-400">{section.title}</h4>
              <ul className="space-y-4">
                {section.links.map((link, i) => (
                  <li key={i}>
                    <Link 
                      to={link.path}
                      className="text-slate-500 hover:text-white text-sm font-bold transition-colors uppercase tracking-widest"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Contact Information */}
          <div className="space-y-6">
            <h4 className="text-xs font-black uppercase tracking-[0.3em] text-blue-400">Contact</h4>
            <ul className="space-y-4">
              <li>
                <a href="mailto:mounibwassimm@gmail.com" className="flex items-center gap-4 group text-slate-500 hover:text-white transition-colors">
                  <div className="p-2 bg-white/5 rounded-lg border border-white/10 group-hover:bg-blue-500/10 transition-colors">
                    <Mail size={16} className="text-blue-500" />
                  </div>
                  <span className="text-sm font-bold tracking-tight">mounibwassimm@gmail.com</span>
                </a>
              </li>
              <li>
                <div className="flex items-center gap-4 text-slate-500">
                  <div className="p-2 bg-white/5 rounded-lg border border-white/10">
                    <Phone size={16} className="text-blue-500" />
                  </div>
                  <a href="https://wa.me/601111769636" target="_blank" rel="noopener noreferrer" className="text-sm font-bold tracking-tight hover:text-blue-400 transition-colors">+60 01111769636</a>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-20 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-slate-600 text-[10px] font-black uppercase tracking-[0.4em]">
            © 2026 CineWhy Architecture. Project High Fidelity.
          </p>
          <div className="flex items-center gap-4 text-slate-600">
             <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
             <span className="text-[10px] font-black uppercase tracking-widest leading-none">Global Server Active</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
