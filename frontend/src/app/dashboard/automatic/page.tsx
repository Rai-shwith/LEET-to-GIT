'use client';
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
