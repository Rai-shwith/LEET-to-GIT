'use client';
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
