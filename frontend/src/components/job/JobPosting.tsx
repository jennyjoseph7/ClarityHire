import React, { useState } from 'react';
import axios from 'axios';
import { Briefcase, Send, MapPin, Building, AlignLeft, Sparkles } from 'lucide-react';

const JobPosting = ({ onJobCreated }: { onJobCreated: () => void }) => {
    const [loading, setLoading] = useState(false);
    const [jobData, setJobData] = useState({
        title: '',
        company: '',
        location: 'Remote',
        description: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const token = localStorage.getItem('access_token');
            await axios.post('http://localhost:8000/api/v1/jobs/', jobData, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            setJobData({ title: '', company: '', location: 'Remote', description: '' });
            onJobCreated();
            alert('Mission Accomplished! Job posted and analyzed.');
        } catch (error) {
            console.error('Error posting job:', error);
            alert('Sync failed. Deployment error.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-10 space-y-10">
            <div className="flex items-center justify-between">
                <div className="space-y-1">
                    <h2 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
                        <Sparkles className="text-red-500 w-8 h-8" />
                        Neural Requisition
                    </h2>
                    <p className="text-zinc-500 text-xs font-bold uppercase tracking-[0.2em]">Deploy high-priority opportunities</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="space-y-2 group">
                        <label className="text-[10px] font-black text-zinc-500 uppercase tracking-widest ml-1 group-focus-within:text-red-500 transition-colors flex items-center gap-2">
                            <Briefcase className="w-3 h-3" />
                            Job Designation
                        </label>
                        <input
                            type="text"
                            required
                            className="w-full bg-black border border-zinc-800 rounded-2xl py-4 px-5 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all text-zinc-100 placeholder:text-zinc-800"
                            placeholder="e.g. Lead Machine Learning Engineer"
                            value={jobData.title}
                            onChange={(e) => setJobData({ ...jobData, title: e.target.value })}
                        />
                    </div>
                    <div className="space-y-2 group">
                        <label className="text-[10px] font-black text-zinc-500 uppercase tracking-widest ml-1 group-focus-within:text-red-500 transition-colors flex items-center gap-2">
                            <Building className="w-3 h-3" />
                            Organization
                        </label>
                        <input
                            type="text"
                            required
                            className="w-full bg-black border border-zinc-800 rounded-2xl py-4 px-5 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all text-zinc-100 placeholder:text-zinc-800"
                            placeholder="e.g. Neural Dynamics Corp"
                            value={jobData.company}
                            onChange={(e) => setJobData({ ...jobData, company: e.target.value })}
                        />
                    </div>
                </div>

                <div className="space-y-2 group">
                    <label className="text-[10px] font-black text-zinc-500 uppercase tracking-widest ml-1 group-focus-within:text-red-500 transition-colors flex items-center gap-2">
                        <MapPin className="w-3 h-3" />
                        Deployment Zone
                    </label>
                    <input
                        type="text"
                        className="w-full bg-black border border-zinc-800 rounded-2xl py-4 px-5 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all text-zinc-100 placeholder:text-zinc-800"
                        placeholder="e.g. Global Remote / Neo-Tokyo"
                        value={jobData.location}
                        onChange={(e) => setJobData({ ...jobData, location: e.target.value })}
                    />
                </div>

                <div className="space-y-2 group">
                    <label className="text-[10px] font-black text-zinc-500 uppercase tracking-widest ml-1 group-focus-within:text-red-500 transition-colors flex items-center gap-2">
                        <AlignLeft className="w-3 h-3" />
                        Requisition Details
                    </label>
                    <textarea
                        required
                        rows={8}
                        className="w-full bg-black border border-zinc-800 rounded-2xl py-4 px-5 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all text-zinc-100 placeholder:text-zinc-800 resize-none leading-relaxed"
                        placeholder="Input the full job description. Our engine will synthesize the required skill matrix automatically."
                        value={jobData.description}
                        onChange={(e) => setJobData({ ...jobData, description: e.target.value })}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-5 rounded-2xl font-black text-sm uppercase tracking-[0.2em] transition-all shadow-xl flex items-center justify-center gap-3 relative overflow-hidden group ${loading
                            ? 'bg-zinc-900 text-zinc-700 cursor-not-allowed border border-zinc-800'
                            : 'bg-red-600 text-white hover:bg-red-700 active:scale-[0.98] shadow-red-600/30'
                        }`}
                >
                    {loading ? (
                        <>
                            <div className="w-5 h-5 border-3 border-white/20 border-t-white rounded-full animate-spin" />
                            Synthesizing...
                        </>
                    ) : (
                        <>
                            <Send className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                            Deploy & Analyze Requisition
                        </>
                    )}
                </button>
            </form>
        </div>
    );
};

export default JobPosting;
