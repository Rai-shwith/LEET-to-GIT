import React from 'react';

export function Badge({ children, variant = 'Easy' }: { children: React.ReactNode, variant?: 'Easy' | 'Medium' | 'Hard' }) {
  const colors = {
    Easy: 'bg-[#10B981] text-[#0A0A1A]',
    Medium: 'bg-[#F59E0B] text-[#0A0A1A]',
    Hard: 'bg-[#EF4444] text-white',
  };
  return <span className={`px-2 py-1 text-xs font-bold rounded ${colors[variant]}`}>{children}</span>;
}
