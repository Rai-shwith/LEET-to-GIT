"use client";
import React from "react";
import { Button } from "../components/ui/Button";
import { GlassCard } from "../components/ui/GlassCard";
import { BACKEND_URL } from "../lib/api";
import {
  GitBranch,
  Zap,
  Edit3,
  BookOpen,
  ChevronRight,
  Terminal,
} from "lucide-react";

export default function LandingPage() {
  const login = () => {
    window.location.href = `${BACKEND_URL}/api/auth/login`;
  };

  return (
    <div className="flex flex-col min-h-screen relative z-0">
      {/* Navbar */}
      <nav className="w-full flex items-center justify-between py-6 px-6 md:px-12 max-w-[1400px] mx-auto">
        <div className="text-xl md:text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#4F46E5] to-[#06B6D4] flex items-center gap-2">
          <GitBranch className="text-[#4F46E5]" size={24} />
          LEET2GIT
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-[#94A3B8]">
          <a href="#features" className="hover:text-white transition-colors">
            Features
          </a>
          <a
            href="#how-it-works"
            className="hover:text-white transition-colors"
          >
            How It Works
          </a>
          <a href="#demo" className="hover:text-white transition-colors">
            Demo
          </a>
        </div>

        <Button
          variant="secondary"
          className="hidden md:flex px-5 py-2 text-sm !font-medium"
          onClick={() =>
            window.open("https://github.com/ashwith/LEET2GIT", "_blank")
          }
        >
          View Repository <ChevronRight size={16} />
        </Button>
      </nav>

      <main className="flex-1 flex flex-col justify-center px-6 md:px-12 w-full max-w-[1400px] mx-auto pb-24">
        {/* Split Hero Section */}
        <div className="flex flex-col lg:flex-row items-center justify-between gap-16 mt-12 lg:mt-24 w-full">
          {/* Left Column - Typography & CTAs */}
          <div className="flex-1 text-left flex flex-col items-start z-10 w-full max-w-2xl">
            <h1 className="text-5xl sm:text-6xl lg:text-[5rem] font-extrabold tracking-tight text-white leading-[1.1] mb-6">
              Sync LeetCode{" "}
              <span className="text-white opacity-80">to GitHub.</span>
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#4F46E5] via-[#7C3AED] to-[#06B6D4]">
                Zero Effort.
              </span>
            </h1>

            <p className="text-lg md:text-xl text-[#94A3B8] mb-10 leading-relaxed font-light max-w-xl">
              LEET2GIT is a seamless integration that pushes your LeetCode
              solutions directly to your GitHub repository. Beautiful READMEs,
              organized code, automated tracking.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
              <Button
                onClick={login}
                variant="primary"
                className="w-full sm:w-auto px-8 py-3.5 text-base"
              >
                Connect with GitHub
              </Button>
              <Button
                variant="secondary"
                className="w-full sm:w-auto px-8 py-3.5 text-base"
                onClick={() =>
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Explore Features <ChevronRight size={18} />
              </Button>
            </div>
          </div>

          {/* Right Column - Terminal Visual */}
          <div className="flex-1 w-full max-w-xl lg:max-w-none relative mt-12 lg:mt-0">
            {/* Ambient Background Glow for Terminal */}
            <div className="absolute inset-0 bg-gradient-to-r from-[#4F46E5]/20 to-[#06B6D4]/20 blur-[100px] -z-10 rounded-[3rem] transform scale-110"></div>

            <GlassCard className="p-0 !rounded-2xl border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] bg-[#0B0B16]/90 backdrop-blur-xl overflow-hidden">
              {/* Terminal Header */}
              <div className="flex items-center px-4 py-3 border-b border-white/5 bg-white/[0.02]">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-[#EF4444]"></div>
                  <div className="w-3 h-3 rounded-full bg-[#F59E0B]"></div>
                  <div className="w-3 h-3 rounded-full bg-[#10B981]"></div>
                </div>
                <div className="flex-1 flex justify-center text-xs text-[#94A3B8]/70 font-mono tracking-wider items-center gap-2 pr-10">
                  leet2git-sync
                </div>
              </div>

              {/* Terminal Body */}
              <div className="p-6 font-mono text-[13px] md:text-sm leading-loose overflow-hidden">
                <div className="text-[#94A3B8] mb-1">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>
                  Connecting to GitHub API...
                </div>
                <div className="text-[#10B981] mb-3">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>✓
                  Authenticated as ashwith
                </div>

                <div className="text-[#94A3B8] mb-1">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>
                  Fetching submissions from LeetCode...
                </div>
                <div className="text-[#06B6D4] mb-3">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>✓ Found 142
                  accepted solutions
                </div>

                <div className="text-[#94A3B8] mb-1">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>
                  Pushing to ashwith/LeetCode-Solutions...
                </div>
                <div className="text-[#10B981] mb-4">
                  <span className="text-[#4F46E5] mr-2">{">"}</span>✓ Commit
                  successful: "Add LRU Cache (Hard)"
                </div>

                <div className="flex items-center text-[#94A3B8]">
                  <span className="text-[#06B6D4] mr-2">~</span>
                  <span className="w-2 h-4 bg-[#06B6D4] animate-[pulse_1s_ease-in-out_infinite] inline-block"></span>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Features Section */}
        <div
          id="features"
          className="w-full mt-32 md:mt-48 grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 pb-12"
        >
          <GlassCard className="p-8 hover:-translate-y-2 transition-transform duration-300 bg-[#0B0B16]/50">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#F59E0B]/20 to-[#F59E0B]/5 flex items-center justify-center mb-6 border border-[#F59E0B]/20 shadow-[0_0_15px_rgba(245,158,11,0.1)]">
              <Zap className="text-[#F59E0B]" size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 text-white tracking-wide">
              Automatic Sync
            </h3>
            <p className="text-[#94A3B8] leading-relaxed font-light">
              Scrape all your submissions instantly using our secure WebSocket
              connection. Populate your repository in one go.
            </p>
          </GlassCard>

          <GlassCard className="p-8 hover:-translate-y-2 transition-transform duration-300 bg-[#0B0B16]/50">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#06B6D4]/20 to-[#06B6D4]/5 flex items-center justify-center mb-6 border border-[#06B6D4]/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]">
              <Edit3 className="text-[#06B6D4]" size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 text-white tracking-wide">
              Manual Submit
            </h3>
            <p className="text-[#94A3B8] leading-relaxed font-light">
              Curating your repo? Paste individual solutions and have them
              beautifully formatted and pushed instantly.
            </p>
          </GlassCard>

          <GlassCard className="p-8 hover:-translate-y-2 transition-transform duration-300 bg-[#0B0B16]/50">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#7C3AED]/20 to-[#7C3AED]/5 flex items-center justify-center mb-6 border border-[#7C3AED]/20 shadow-[0_0_15px_rgba(124,58,237,0.1)]">
              <BookOpen className="text-[#7C3AED]" size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3 text-white tracking-wide">
              Beautiful READMEs
            </h3>
            <p className="text-[#94A3B8] leading-relaxed font-light">
              Auto-generated markdown files with full problem descriptions,
              dynamic difficulty badges, and clean code blocks.
            </p>
          </GlassCard>
        </div>
      </main>
    </div>
  );
}
