'use client';
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
