import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { ContactShadows, Environment, PerspectiveCamera, Float } from '@react-three/drei';
import { motion } from 'framer-motion';
import * as THREE from 'three';
import { Shield, Zap, BarChart3, ChevronDown, Play } from 'lucide-react';
import logo from "../assets/logo.png";

const bubbleColors = ['#00d4ff', '#ff4bff', '#7b61ff', '#3b82f6'];

const Bubbles = () => {
  const bubbles = Array.from({ length: 12 }).map((_, i) => ({
    position: [
      (Math.random() - 0.5) * 25, 
      (Math.random() - 0.5) * 25, 
      (Math.random() - 0.5) * 15 - 5
    ] as [number, number, number],
    speed: Math.random() * 0.005 + 0.002,
    offset: Math.random() * Math.PI * 2,
    size: Math.random() * 0.9 + 0.3,
    color: bubbleColors[i % bubbleColors.length]
  }));

  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    if (groupRef.current) {
      groupRef.current.children.forEach((bubble: any, i) => {
        const config = bubbles[i];
        // Omnidirectional floating using sine/cosine offsets, untethered from scroll physics
        bubble.position.y += Math.sin(time * 0.5 + config.offset) * config.speed;
        bubble.position.x += Math.cos(time * 0.3 + config.offset) * config.speed;
        bubble.position.z += Math.sin(time * 0.4 + config.offset) * config.speed * 0.5;
        // Keep them bounded softly
        if (bubble.position.y > 15) bubble.position.y = -15;
        if (bubble.position.x > 18) bubble.position.x -= 36;
        if (bubble.position.x < -18) bubble.position.x += 36;
      });
    }
  });

  return (
    <group ref={groupRef}>
      {bubbles.map((config, i) => (
        <mesh key={i} position={config.position}>
          <sphereGeometry args={[config.size, 32, 32]} />
          <meshPhysicalMaterial 
            color={config.color} 
            emissive={config.color}
            emissiveIntensity={0.6}
            transmission={0.8} 
            opacity={0.9} 
            transparent 
            roughness={0.1} 
            ior={1.4}
            thickness={1}
          />
        </mesh>
      ))}
    </group>
  );
};

const Scene = () => {
  const { gl } = useThree();
  useEffect(() => {
    return () => { gl.dispose(); };
  }, [gl]);

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 0, 20]} />
      <Environment preset="night" />
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={2} color="#3b82f6" />
      <pointLight position={[-10, -10, 10]} intensity={1} color="#8b5cf6" />
      <Bubbles />
      <ContactShadows position={[0, -12, 0]} opacity={0.3} scale={40} blur={3} far={15} />
    </>
  );
};

const BenefitCard = ({ title, desc, icon: Icon, delay }: { title: string, desc: string, icon: any, delay: number }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.6 }}
      whileHover={{ y: -10, scale: 1.02 }}
      className="card-3d group p-8 flex flex-col items-center text-center space-y-4"
    >
      <div className="w-16 h-16 rounded-2xl bg-blue-500/10 flex items-center justify-center text-blue-400 group-hover:scale-110 group-hover:bg-blue-500/20 transition-all duration-500 shadow-xl">
        <Icon size={32} />
      </div>
      <h3 className="text-2xl font-poppins font-black text-white">{title}</h3>
      <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
    </motion.div>
  );
};

const WelcomeDashboard: React.FC<{ onStart: () => void }> = ({ onStart }) => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const scrollToContent = () => {
    const nextSection = document.getElementById('benefits-section');
    nextSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="relative w-full min-h-screen bg-[#0f0c29] text-white flex flex-col items-center overflow-x-hidden dashboard-page">
      {/* Top bar removed, branding is now in Sidebar */}

      <section className="relative w-full h-screen flex flex-col items-center justify-center pt-20 px-8">
        <div className="absolute inset-x-0 top-0 h-full z-0 pointer-events-none">
          <Canvas shadows gl={{ antialias: true }}>
            <Scene />
          </Canvas>
        </div>

        <div className="relative z-10 flex flex-col items-center text-center">
          <h2 className="cinematic-title">
            <span className="cinematic-white">CINEMATIC </span> 
            <span className="cinematic-color">LOGIC</span>
          </h2>

          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-lg md:text-2xl text-slate-400 max-w-2xl mx-auto leading-relaxed mb-8 md:mb-12 px-4"
          >
            Elevate your cinematic journey with our pure rule-based engine. 
            Experience logic through a premium 3D lens.
          </motion.p>

          <div className="flex flex-col gap-6 md:gap-12 items-center w-full px-4">
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onStart}
              className="btn-premium text-lg md:text-2xl px-8 md:px-12 py-4 md:py-6 flex items-center gap-4 group w-full md:w-auto"
            >
              Start Discovery
              <Play size={20} className="fill-current group-hover:translate-x-1 transition-transform" />
            </motion.button>
            
            <div className="flex flex-col items-center gap-3">
              <motion.button 
                onClick={scrollToContent}
                className="btn-discover-3d"
              >
                Discover More
              </motion.button>
              <motion.div
                animate={{ y: [0, 8, 0], opacity: [0.5, 1, 0.5] }}
                transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
                className="text-blue-500 font-bold"
              >
                ↓
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      <section id="benefits-section" className="relative w-full max-w-7xl px-8 py-32 space-y-24">
        <div className="flex flex-col items-center text-center space-y-4">
          <h2 className="text-4xl md:text-6xl font-poppins font-black">THE BASICS</h2>
          <div className="w-24 h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <BenefitCard icon={Shield} title="Sovereign Logic" desc="Our pure rule-based engine operates without hidden biases, putting you in complete control." delay={0.1} />
          <BenefitCard icon={BarChart3} title="Neural Insights" desc="Deep analytics provide a transparent view into why every single movie matches your profile." delay={0.2} />
          <BenefitCard icon={Zap} title="Instant Retrieval" desc="Blazing fast search and sub-millisecond recommendation generation." delay={0.3} />
        </div>
      </section>
    </div>
  );
};

export default WelcomeDashboard;
