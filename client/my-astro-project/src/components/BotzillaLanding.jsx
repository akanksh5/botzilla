/*
  File: src/components/BotzillaLanding.jsx
*/

import React from "react";

const BotzillaLanding = () => {
  return (
    <div className="relative min-h-screen bg-gradient-to-b from-black via-indigo-950 to-purple-950 text-white overflow-hidden font-sans">
      {/* Starry Background */}
      <div className="absolute inset-0 z-0 bg-[url('/stars.svg')] bg-cover bg-center opacity-20 animate-pulse" />
{/* Twinkling Stars Layer */}
<div className="absolute inset-0 z-0 overflow-hidden">
  {Array.from({ length: 60 }).map((_, i) => {
    const top = Math.random() * 100;
    const left = Math.random() * 100;
    const delay = Math.random() * 5;
    return (
      <div
        key={i}
        className="absolute w-1 h-1 bg-white rounded-full opacity-80 animate-twinkle"
        style={{
          top: `${top}%`,
          left: `${left}%`,
          animationDelay: `${delay}s`,
        }}
      />
    );
  })}
</div>

      {/* Glowing Planets */}
      <div className="absolute top-10 left-10 w-72 h-72 bg-purple-700 rounded-full blur-3xl opacity-30 animate-ping" />
      <div className="absolute bottom-20 right-20 w-64 h-64 bg-indigo-600 rounded-full blur-2xl opacity-40 animate-pulse" />

      {/* Hero Content */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center px-6 py-32">
        <h1 className="text-6xl sm:text-7xl font-extrabold text-white drop-shadow-[0_0_20px_rgba(168,85,247,0.8)]">
          🔾 Botzilla
        </h1>
        <p className="mt-6 text-xl max-w-2xl text-purple-200">
          The space-age Slack bot that boosts mental well-being and minimizes meeting madness – built for your remote galaxy.
        </p>

        {/* CTA Button */}
        <a
          href="https://slack.com/oauth/v2/authorize?client_id=YOUR_CLIENT_ID"
          className="mt-10 inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-700 to-indigo-600 hover:from-purple-600 hover:to-indigo-500 text-white text-lg font-semibold rounded-xl shadow-lg ring-2 ring-purple-500 hover:ring-indigo-400 transition-all duration-300 animate-glow"
        >
          🚀 Add Botzilla to Slack
        </a>

        {/* Floating Rocket */}
        <img
          src="/rocket.svg"
          alt="Rocket"
          className="mt-16 w-32 md:w-40 animate-bounce hover:scale-110 transition duration-300"
        />
      </div>

      {/* Footer */}
      <footer className="relative z-10 text-center text-sm text-purple-300 mt-24 pb-12">
        Made with ❤️ in the Milky Way · © 2025 Botzilla
      </footer>
    </div>
  );
};

export default BotzillaLanding;
