'use client';
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
