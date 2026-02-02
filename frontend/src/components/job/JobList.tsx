import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Target, MapPin, Building2, Flame, Layers } from 'lucide-react';

const JobList = ({ refresh }: { refresh: boolean }) => {
    const [jobs, setJobs] = useState<any[]>([]);
    const [matches, setMatches] = useState<Record<string, number>>({});
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('access_token');
            if (!token || token === 'undefined') {
                setLoading(false);
                return;
            }
            const headers = { 'Authorization': `Bearer ${token}` };

            const jobsRes = await axios.get('http://localhost:8000/api/v1/jobs/', { headers });
            setJobs(jobsRes.data);

            const resumeRes = await axios.get('http://localhost:8000/api/v1/resumes/mine/latest', { headers });
            const resume = resumeRes.data;

            if (resume && resume.id) {
                const matchRes = await axios.get(`http://localhost:8000/api/v1/matches/resume/${resume.id}`, { headers });
                const matchMap: Record<string, number> = {};
                matchRes.data.forEach((m: any) => {
                    matchMap[m.job_id] = m.score;
                });
                setMatches(matchMap);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        console.log("JobList Effect Triggered. Refresh:", refresh);
        fetchData();
        return () => console.log("JobList Cleanup/Unmount");
    }, [refresh]);

    if (loading) return (
        <div className="flex flex-col items-center justify-center p-20 space-y-4">
            <div className="w-12 h-12 border-4 border-red-600/20 border-t-red-600 rounded-full animate-spin" />
            <p className="text-zinc-500 font-bold uppercase tracking-widest text-xs">Scanning Matrix...</p>
        </div>
    );

    const getScoreStyles = (score: number) => {
        if (score >= 80) return {
            bg: 'bg-emerald-500/10',
            text: 'text-emerald-400',
            border: 'border-emerald-500/20',
            shadow: 'shadow-emerald-500/20'
        };
        if (score >= 50) return {
            bg: 'bg-amber-500/10',
            text: 'text-amber-400',
            border: 'border-amber-500/20',
            shadow: 'shadow-amber-500/20'
        };
        return {
            bg: 'bg-red-500/10',
            text: 'text-red-400',
            border: 'border-red-500/20',
            shadow: 'shadow-red-500/20'
        };
    };

    return (
        <div className="p-6 space-y-8 h-full min-h-[600px]">
            <div className="flex justify-between items-end border-b border-zinc-800 pb-6">
                <div>
                    <h2 className="text-3xl font-black text-white tracking-tight flex items-center gap-2">
                        <Target className="text-red-600 w-8 h-8" />
                        Available Nodes
                    </h2>
                    <p className="text-zinc-500 text-sm mt-1">Found {jobs.length} relevant matches for your profile</p>
                </div>
            </div>

            {jobs.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-20 bg-zinc-900/20 border border-zinc-800 rounded-3xl border-dashed">
                    <p className="text-zinc-600 font-bold uppercase tracking-widest">No active nodes detected</p>
                </div>
            ) : (
                <div className="grid gap-6">
                    {jobs.map((job) => {
                        const score = matches[job.id];
                        const styles = score !== undefined ? getScoreStyles(score) : null;

                        return (
                            <div key={job.id} className="group relative p-6 bg-zinc-900/40 border border-zinc-800 hover:border-red-600/30 rounded-3xl transition-all duration-500 hover:shadow-2xl hover:shadow-red-600/5">
                                <div className="flex justify-between items-start gap-4">
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2.5 bg-zinc-800 rounded-xl group-hover:bg-red-600/10 transition-colors">
                                                <Building2 className="w-5 h-5 text-zinc-400 group-hover:text-red-500 transition-colors" />
                                            </div>
                                            <h3 className="font-black text-xl text-zinc-100 group-hover:text-white transition-colors">{job.title}</h3>
                                        </div>

                                        <div className="flex items-center gap-4 text-xs font-bold uppercase tracking-widest text-zinc-500">
                                            <div className="flex items-center gap-1.5 text-red-500/70">
                                                <Flame className="w-3.5 h-3.5" />
                                                {job.company}
                                            </div>
                                            <div className="flex items-center gap-1.5">
                                                <MapPin className="w-3.5 h-3.5" />
                                                {job.location}
                                            </div>
                                        </div>

                                        <p className="text-zinc-500 text-sm line-clamp-2 leading-relaxed max-w-xl">
                                            {job.description}
                                        </p>
                                    </div>

                                    {score !== undefined ? (
                                        <div className={`flex flex-col items-center justify-center w-24 h-24 rounded-2xl border-2 ${styles?.bg} ${styles?.border} ${styles?.shadow} shadow-lg transition-transform duration-500 group-hover:scale-105`}>
                                            <span className={`text-3xl font-black ${styles?.text}`}>{score}%</span>
                                            <span className="text-[8px] font-black uppercase tracking-[0.2em] opacity-60">Match</span>
                                        </div>
                                    ) : (
                                        <div className="flex flex-col items-center justify-center w-24 h-24 rounded-2xl border border-zinc-800 bg-zinc-800/20 opacity-40">
                                            <Layers className="w-6 h-6 text-zinc-500 mb-1" />
                                            <span className="text-[8px] font-black uppercase tracking-widest">Pending</span>
                                        </div>
                                    )}
                                </div>

                                <div className="mt-8 flex flex-wrap gap-2">
                                    {job.parsed_requirements?.required_skills?.slice(0, 5).map((skill: string, i: number) => (
                                        <span key={i} className="bg-zinc-800/80 text-zinc-300 text-[10px] font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full border border-zinc-700/50 group-hover:border-red-500/20 transition-colors">
                                            {skill}
                                        </span>
                                    ))}
                                    {job.parsed_requirements?.required_skills?.length > 5 && (
                                        <span className="text-zinc-600 text-[10px] font-black uppercase ml-1 flex items-center italic">
                                            +{job.parsed_requirements.required_skills.length - 5} more
                                        </span>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default JobList;
