'use client';
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
