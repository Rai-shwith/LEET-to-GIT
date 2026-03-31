export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

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
