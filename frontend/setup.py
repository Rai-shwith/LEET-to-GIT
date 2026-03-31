import os

FILES = {
    ".env.local.example": """NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
""",
    "vercel.json": """{
  "buildCommand": "npm run build",
  "installCommand": "npm install",
  "framework": "nextjs"
}
""",
    "src/middleware.ts": """import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token');
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/', request.url));
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
""",
    "src/lib/api.ts": """export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function getMe() {
  const res = await fetch(`${BACKEND_URL}/auth/me`, { credentials: 'include' });
  if (!res.ok) throw new Error('Not authenticated');
  return res.json();
}

export async function logout() {
  const res = await fetch(`${BACKEND_URL}/auth/logout`, { method: 'POST', credentials: 'include' });
  if (!res.ok) throw new Error('Logout failed');
  return res.json();
}

export async function manualUpload(payload: any) {
  const res = await fetch(`${BACKEND_URL}/upload/manual/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}
""",
    "src/lib/ws.ts": """export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export function createAutomaticWS() {
  const wsUrl = BACKEND_URL.replace(/^http/, 'ws') + '/upload/ws/automatic/';
  return new WebSocket(wsUrl);
}
""",
    "src/hooks/useAuth.ts": """'use client';
import { useState, useEffect } from 'react';
import { getMe } from '../lib/api';
import { useRouter } from 'next/navigation';

export function useAuth() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const router = useRouter();

  useEffect(() => {
    getMe()
      .then(setUser)
      .catch((err) => {
        setError(err);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  return { user, loading, error };
}
""",
    "src/components/ui/GlassCard.tsx": """import React from 'react';

export function GlassCard({ children, className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.10)] backdrop-blur-[12px] rounded-xl ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
""",
    "src/components/ui/Button.tsx": """import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
}

export function Button({ variant = 'primary', className = '', children, ...props }: ButtonProps) {
  const base = 'px-4 py-2 rounded-md font-medium transition-colors';
  const variants = {
    primary: 'bg-[#4F46E5] hover:bg-[#4338CA] text-white',
    secondary: 'bg-[#7C3AED] hover:bg-[#6D28D9] text-white',
    danger: 'bg-[#EF4444] hover:bg-[#DC2626] text-white',
  };
  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
""",
    "src/components/ui/Badge.tsx": """import React from 'react';

export function Badge({ children, variant = 'Easy' }: { children: React.ReactNode, variant?: 'Easy' | 'Medium' | 'Hard' }) {
  const colors = {
    Easy: 'bg-[#10B981] text-[#0A0A1A]',
    Medium: 'bg-[#F59E0B] text-[#0A0A1A]',
    Hard: 'bg-[#EF4444] text-white',
  };
  return <span className={`px-2 py-1 text-xs font-bold rounded ${colors[variant]}`}>{children}</span>;
}
""",
    "src/components/ui/Spinner.tsx": """import React from 'react';
import { Loader2 } from 'lucide-react';

export function Spinner({ className = '' }: { className?: string }) {
  return <Loader2 className={`animate-spin ${className}`} />;
}
""",
    "src/components/ui/CodeBlock.tsx": """'use client';
import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';

export function CodeBlock({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);

  const copy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative bg-[#0D1117] p-4 rounded-md font-mono text-[#06B6D4] text-sm overflow-x-auto">
      <button onClick={copy} className="absolute top-2 right-2 p-1 bg-white/10 rounded hover:bg-white/20">
        {copied ? <Check size={16} /> : <Copy size={16} />}
      </button>
      <pre><code>{code}</code></pre>
    </div>
  );
}
""",
    "src/components/Navbar.tsx": """'use client';
import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { logout } from '../lib/api';
import { useRouter } from 'next/navigation';

export function Navbar() {
  const { user } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <nav className="flex items-center justify-between p-4 bg-[#0F172A] border-b border-[#2D2D5E]">
      <div className="text-xl font-bold text-white">LEET2GIT</div>
      {user && (
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            {user.avatar_url && <img src={user.avatar_url} alt="Avatar" className="w-8 h-8 rounded-full" />}
            <span className="text-[#94A3B8]">{user.login}</span>
          </div>
          <button onClick={handleLogout} className="text-sm text-[#EF4444] hover:underline">Logout</button>
        </div>
      )}
    </nav>
  );
}
""",
    "src/components/ProgressFeed.tsx": """import React, { useEffect, useRef } from 'react';

export function ProgressFeed({ messages }: { messages: string[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="bg-[#0A0A1A] border-l-4 border-[#4F46E5] p-4 font-mono text-sm h-64 overflow-y-auto mt-4 rounded-r-md">
      {messages.map((m, i) => (
        <div key={i} className="text-[#94A3B8] mb-1">{'>'} {m}</div>
      ))}
      <div className="text-[#06B6D4] animate-pulse">_</div>
      <div ref={bottomRef} />
    </div>
  );
}
""",
    "src/app/layout.tsx": """import './globals.css';
import React from 'react';

export const metadata = {
  title: 'LEET2GIT',
  description: 'Sync LeetCode to GitHub',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0A0A1A] text-white min-h-screen">
        {children}
      </body>
    </html>
  );
}
""",
    "src/app/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: #0A0A1A;
  color: #FFFFFF;
}
""",
    "src/app/page.tsx": """'use client';
import React from 'react';
import { Button } from '../components/ui/Button';
import { GlassCard } from '../components/ui/GlassCard';
import { BACKEND_URL } from '../lib/api';
import { Github, Zap, Edit3, BookOpen } from 'lucide-react';

export default function LandingPage() {
  const login = () => {
    window.location.href = `${BACKEND_URL}/auth/login`;
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#0A0A1A]">
      <main className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight text-white">
          Sync LeetCode <span className="text-[#4F46E5]">→</span> GitHub.<br/>Automatically.
        </h1>
        <p className="text-xl text-[#94A3B8] max-w-2xl mb-10">
          Connect your account, write your solutions, and let us handle the rest. Beautiful READMEs, organized code, zero effort.
        </p>
        <Button onClick={login} className="text-lg px-8 py-4 flex items-center gap-2" variant="primary">
          <Github /> Connect with GitHub
        </Button>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 max-w-5xl w-full text-left">
          <GlassCard className="p-6">
            <Zap className="text-[#F59E0B] mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2 text-white">Automatic Sync</h3>
            <p className="text-[#94A3B8]">Scrape all your submissions instantly using our secure WebSocket connection.</p>
          </GlassCard>
          <GlassCard className="p-6">
            <Edit3 className="text-[#06B6D4] mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2 text-white">Manual Submit</h3>
            <p className="text-[#94A3B8]">Want to curate your repo? Submit solutions one by one manually.</p>
          </GlassCard>
          <GlassCard className="p-6">
            <BookOpen className="text-[#7C3AED] mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2 text-white">Beautiful READMEs</h3>
            <p className="text-[#94A3B8]">Auto-generated markdown files with problem descriptions and your solutions.</p>
          </GlassCard>
        </div>
      </main>
      <footer className="p-6 text-center text-[#94A3B8] border-t border-[#2D2D5E]">
        <a href="https://github.com/ashwith/LEET2GIT" className="hover:text-white flex justify-center items-center gap-2">
          <Github size={16} /> View on GitHub
        </a>
      </footer>
    </div>
  );
}
""",
    "src/app/auth/callback/page.tsx": """'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Spinner } from '../../../components/ui/Spinner';

export default function AuthCallback() {
  const router = useRouter();

  useEffect(() => {
    router.push('/dashboard');
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Spinner className="w-12 h-12 text-[#4F46E5] mb-4" />
      <p className="text-[#94A3B8]">Connecting your GitHub...</p>
    </div>
  );
}
""",
    "src/app/dashboard/layout.tsx": """'use client';
import React, { useEffect } from 'react';
import { Navbar } from '../../components/Navbar';
import { useAuth } from '../../hooks/useAuth';
import { useRouter } from 'next/navigation';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/');
    }
  }, [user, loading, router]);

  if (loading) return <div className="min-h-screen bg-[#0A0A1A]" />;
  if (!user) return null;

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0A1A]">
      <Navbar />
      <main className="flex-1 p-6 max-w-6xl mx-auto w-full">
        {children}
      </main>
    </div>
  );
}
""",
    "src/app/dashboard/page.tsx": """'use client';
import React from 'react';
import { GlassCard } from '../../components/ui/GlassCard';
import { useRouter } from 'next/navigation';
import { Zap, Edit3 } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

export default function Dashboard() {
  const router = useRouter();
  const { user } = useAuth();

  return (
    <div>
      <h2 className="text-3xl font-bold mb-2">Welcome back!</h2>
      {user?.repo_name && (
        <p className="text-[#94A3B8] mb-8">
          Linked Repo: <a href={`https://github.com/${user.login}/${user.repo_name}`} target="_blank" className="text-[#06B6D4] hover:underline">{user.repo_name}</a>
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassCard onClick={() => router.push('/dashboard/automatic')} className="p-8 cursor-pointer hover:border-[#4F46E5] transition-colors group">
          <Zap className="text-[#F59E0B] mb-4 group-hover:scale-110 transition-transform" size={48} />
          <h3 className="text-2xl font-bold mb-2">Automatic Sync</h3>
          <p className="text-[#94A3B8]">Scrape and sync all your existing LeetCode submissions at once.</p>
        </GlassCard>

        <GlassCard onClick={() => router.push('/dashboard/manual')} className="p-8 cursor-pointer hover:border-[#06B6D4] transition-colors group">
          <Edit3 className="text-[#06B6D4] mb-4 group-hover:scale-110 transition-transform" size={48} />
          <h3 className="text-2xl font-bold mb-2">Manual Submit</h3>
          <p className="text-[#94A3B8]">Paste a single solution to sync it to your repository instantly.</p>
        </GlassCard>
      </div>
    </div>
  );
}
""",
    "src/app/dashboard/automatic/page.tsx": """'use client';
import React, { useState, useEffect } from 'react';
import { Button } from '../../../components/ui/Button';
import { GlassCard } from '../../../components/ui/GlassCard';
import { CodeBlock } from '../../../components/ui/CodeBlock';
import { ProgressFeed } from '../../../components/ProgressFeed';
import { createAutomaticWS } from '../../../lib/ws';
import { CheckCircle, AlertCircle } from 'lucide-react';

export default function AutomaticSync() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [snippet, setSnippet] = useState<string>('');
  const [messages, setMessages] = useState<string[]>([]);
  const [status, setStatus] = useState<'idle' | 'connected' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const connect = () => {
    const socket = createAutomaticWS();
    setWs(socket);
    setStatus('connected');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'snippet') setSnippet(data.code);
      if (data.type === 'log') setMessages(m => [...m, data.message]);
      if (data.type === 'success') {
        setStatus('success');
        setMessages(m => [...m, `Success: ${data.message}`]);
      }
      if (data.type === 'error') {
        setStatus('error');
        setErrorMsg(data.message);
      }
    };

    socket.onerror = () => {
      setStatus('error');
      setErrorMsg('WebSocket connection failed');
    };
  };

  useEffect(() => {
    return () => ws?.close();
  }, [ws]);

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Automatic Sync</h2>

      {status === 'idle' && (
        <GlassCard className="p-6 text-center">
          <p className="mb-4 text-[#94A3B8]">Click below to open a secure WebSocket connection and generate your sync snippet.</p>
          <Button onClick={connect}>Connect WebSocket</Button>
        </GlassCard>
      )}

      {status === 'connected' && snippet && (
        <div className="space-y-6">
          <GlassCard className="p-6">
            <h3 className="text-xl font-bold mb-2">Instructions</h3>
            <ol className="list-decimal list-inside text-[#94A3B8] space-y-2 mb-4">
              <li>Open <strong>LeetCode.com</strong> in a new tab.</li>
              <li>Press <kbd className="bg-[#2D2D5E] px-1 rounded">F12</kbd> to open Developer Tools.</li>
              <li>Go to the <strong>Console</strong> tab.</li>
              <li>Paste the snippet below and press Enter.</li>
            </ol>
            <CodeBlock code={snippet} />
          </GlassCard>
          <ProgressFeed messages={messages} />
        </div>
      )}

      {status === 'success' && (
        <GlassCard className="p-6 text-center border-[#10B981]">
          <CheckCircle className="text-[#10B981] mx-auto mb-4 w-16 h-16" />
          <h3 className="text-2xl font-bold mb-2">Sync Complete!</h3>
          <p className="text-[#94A3B8]">Your solutions have been successfully pushed to GitHub.</p>
        </GlassCard>
      )}

      {status === 'error' && (
        <GlassCard className="p-6 text-center border-[#EF4444]">
          <AlertCircle className="text-[#EF4444] mx-auto mb-4 w-16 h-16" />
          <h3 className="text-2xl font-bold mb-2">Sync Failed</h3>
          <p className="text-[#EF4444]">{errorMsg}</p>
        </GlassCard>
      )}
    </div>
  );
}
""",
    "src/app/dashboard/manual/page.tsx": """'use client';
import React, { useState } from 'react';
import { GlassCard } from '../../../components/ui/GlassCard';
import { Button } from '../../../components/ui/Button';
import { Spinner } from '../../../components/ui/Spinner';
import { manualUpload } from '../../../lib/api';

export default function ManualSubmit() {
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{msg: string, type: 'success' | 'error'} | null>(null);
  const [formData, setFormData] = useState({
    problem_number: '',
    title: '',
    difficulty: 'Easy' as 'Easy'|'Medium'|'Hard',
    language: 'Python',
    code: ''
  });

  const showToast = (msg: string, type: 'success' | 'error') => {
    setToast({msg, type});
    setTimeout(() => setToast(null), 3000);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await manualUpload(formData);
      showToast('Solution submitted successfully!', 'success');
      setFormData({...formData, code: ''});
    } catch (err: any) {
      showToast(err.message || 'Submission failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Manual Submit</h2>

      {toast && (
        <div className={`fixed top-4 right-4 p-4 rounded-md font-bold text-white z-50 ${toast.type === 'success' ? 'bg-[#10B981]' : 'bg-[#EF4444]'}`}>
          {toast.msg}
        </div>
      )}

      <GlassCard className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Problem Number</label>
              <input type="number" required value={formData.problem_number} onChange={e => setFormData({...formData, problem_number: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white" />
            </div>
            <div className="flex-[2]">
              <label className="block text-sm text-[#94A3B8] mb-1">Title</label>
              <input type="text" required value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white" />
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Difficulty</label>
              <select value={formData.difficulty} onChange={e => setFormData({...formData, difficulty: e.target.value as any})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white">
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Language</label>
              <select value={formData.language} onChange={e => setFormData({...formData, language: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white">
                <option>Python</option>
                <option>JavaScript</option>
                <option>TypeScript</option>
                <option>Java</option>
                <option>C++</option>
                <option>Go</option>
                <option>Rust</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm text-[#94A3B8] mb-1">Code</label>
            <textarea required rows={10} value={formData.code} onChange={e => setFormData({...formData, code: e.target.value})} className="w-full bg-[#0D1117] text-[#06B6D4] font-mono border border-[#2D2D5E] rounded p-4"></textarea>
          </div>

          <Button type="submit" className="w-full flex justify-center items-center gap-2" disabled={loading}>
            {loading ? <Spinner /> : 'Submit Solution'}
          </Button>
        </form>
      </GlassCard>
    </div>
  );
}
"""
}

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for filepath, content in FILES.items():
        full_path = os.path.join(base_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {filepath}")

    print("\nNext.js frontend setup complete.")
    print("Run `npm install lucide-react` before starting the development server.")

if __name__ == "__main__":
    main()
