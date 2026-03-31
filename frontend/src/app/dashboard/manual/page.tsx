'use client';
import React, { useState } from 'react';
import { GlassCard } from '../../../components/ui/GlassCard';
import { Button } from '../../../components/ui/Button';
import { Spinner } from '../../../components/ui/Spinner';
import { manualUpload } from '../../../lib/api';

export default function ManualSubmit() {
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{msg: string, type: 'success' | 'error'} | null>(null);
  const [formData, setFormData] = useState({
    problem_number: '',
    title: '',
    difficulty: 'Easy' as 'Easy'|'Medium'|'Hard',
    language: 'Python',
    code: ''
  });

  const showToast = (msg: string, type: 'success' | 'error') => {
    setToast({msg, type});
    setTimeout(() => setToast(null), 3000);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await manualUpload(formData);
      showToast('Solution submitted successfully!', 'success');
      setFormData({...formData, code: ''});
    } catch (err: any) {
      showToast(err.message || 'Submission failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Manual Submit</h2>

      {toast && (
        <div className={`fixed top-4 right-4 p-4 rounded-md font-bold text-white z-50 ${toast.type === 'success' ? 'bg-[#10B981]' : 'bg-[#EF4444]'}`}>
          {toast.msg}
        </div>
      )}

      <GlassCard className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Problem Number</label>
              <input type="number" required value={formData.problem_number} onChange={e => setFormData({...formData, problem_number: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white" />
            </div>
            <div className="flex-[2]">
              <label className="block text-sm text-[#94A3B8] mb-1">Title</label>
              <input type="text" required value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white" />
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Difficulty</label>
              <select value={formData.difficulty} onChange={e => setFormData({...formData, difficulty: e.target.value as any})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white">
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-sm text-[#94A3B8] mb-1">Language</label>
              <select value={formData.language} onChange={e => setFormData({...formData, language: e.target.value})} className="w-full bg-[#0A0A1A] border border-[#2D2D5E] rounded p-2 text-white">
                <option>Python</option>
                <option>JavaScript</option>
                <option>TypeScript</option>
                <option>Java</option>
                <option>C++</option>
                <option>Go</option>
                <option>Rust</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm text-[#94A3B8] mb-1">Code</label>
            <textarea required rows={10} value={formData.code} onChange={e => setFormData({...formData, code: e.target.value})} className="w-full bg-[#0D1117] text-[#06B6D4] font-mono border border-[#2D2D5E] rounded p-4"></textarea>
          </div>

          <Button type="submit" className="w-full flex justify-center items-center gap-2" disabled={loading}>
            {loading ? <Spinner /> : 'Submit Solution'}
          </Button>
        </form>
      </GlassCard>
    </div>
  );
}
