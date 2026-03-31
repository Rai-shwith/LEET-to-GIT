'use client';
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
