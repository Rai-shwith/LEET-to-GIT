import React, { useEffect, useRef } from 'react';

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
