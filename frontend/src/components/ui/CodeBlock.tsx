'use client';
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
