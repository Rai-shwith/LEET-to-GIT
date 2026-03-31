export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export function createAutomaticWS() {
  const wsUrl = BACKEND_URL.replace(/^http/, 'ws') + '/upload/ws/automatic/';
  return new WebSocket(wsUrl);
}
