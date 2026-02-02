import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { UploadCloud, FileCheck, AlertCircle, Info, FileText, CheckCircle2 } from 'lucide-react';

const ResumeUpload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<any>(null);

    // Fetch latest resume on mount
    useEffect(() => {
        console.log("ResumeUpload MOUNTED");
        const fetchLatestResume = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) return;

            try {
                const response = await axios.get('http://localhost:8000/api/v1/resumes/mine/latest', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (response.data) {
                    setStatus(response.data);
                }
            } catch (error) {
                console.log("No existing resume found or error fetching.");
            }
        };
        fetchLatestResume();

        return () => console.log("ResumeUpload UNMOUNTED");
    }, []);

    const statusStr = status?.status?.toLowerCase() || '';

    // Polling logic: Only poll if we are in a transitive state (PENDING or PARSING)
    useEffect(() => {
        if (!statusStr || (statusStr !== 'pending' && statusStr !== 'parsing')) {
            return;
        }

        const fetchLatestResume = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) return;

            try {
                const response = await axios.get('http://localhost:8000/api/v1/resumes/mine/latest', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (response.data) {
                    setStatus(response.data);
                }
            } catch (error) {
                console.error("Polling error", error);
            }
        };

        const interval = setInterval(fetchLatestResume, 3000);
        return () => clearInterval(interval);
    }, [statusStr]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const token = localStorage.getItem('access_token');
        if (!token || token === 'undefined') {
            alert('Authentication lost. Please log in again.');
            return;
        }

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/api/v1/resumes/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                },
            });
            setStatus(response.data);
            alert('Upload successful! Neural parsing initiated.');
        } catch (error) {
            console.error('Error uploading resume:', error);
            alert('Upload failed. Connection error.');
        } finally {
            setUploading(false);
        }
    };

    const isParsed = statusStr === 'parsed';
    const isParsing = statusStr === 'parsing' || statusStr === 'pending';

    return (
        <div className="bg-zinc-900/50 backdrop-blur-xl rounded-[2rem] border border-zinc-800/50 p-8 shadow-2xl space-y-8">
            <div className="space-y-1">
                <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
                    <FileText className="text-red-600 w-6 h-6" />
                    Neural Profile
                </h2>
                <p className="text-zinc-500 text-xs font-bold uppercase tracking-widest">
                    Synchronize your skills matrix
                </p>
            </div>

            <div className="space-y-6">
                {!isParsed ? (
                    <label className="relative flex flex-col items-center justify-center w-full h-56 border-2 border-dashed border-zinc-800 rounded-[1.5rem] cursor-pointer bg-black/40 hover:bg-black/60 hover:border-red-600/40 transition-all group overflow-hidden">
                        {/* Background Pulse Effect */}
                        <div className="absolute inset-0 bg-red-600/0 group-hover:bg-red-600/5 transition-colors duration-500" />

                        <div className="relative flex flex-col items-center justify-center pt-5 pb-6 px-4 text-center">
                            <div className="w-16 h-16 mb-4 bg-zinc-900 rounded-2xl flex items-center justify-center border border-zinc-800 group-hover:border-red-600/50 group-hover:shadow-lg group-hover:shadow-red-600/10 transition-all">
                                <UploadCloud className="w-8 h-8 text-zinc-500 group-hover:text-red-500 transition-colors" />
                            </div>
                            <p className="mb-2 text-sm text-zinc-300 font-bold tracking-tight">
                                {file ? file.name : 'Inject Profile Source'}
                            </p>
                            <p className="text-[10px] text-zinc-500 font-black uppercase tracking-[0.2em]">PDF Standard • Max 5MB</p>
                        </div>
                        <input type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
                    </label>
                ) : (
                    <div className="p-6 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex flex-col gap-6 animate-in fade-in zoom-in duration-500">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-emerald-500/20 rounded-full">
                                <CheckCircle2 className="w-8 h-8 text-emerald-500" />
                            </div>
                            <div className="flex-1">
                                <p className="text-white font-bold text-lg">Analysis Complete</p>
                                <p className="text-emerald-500/70 text-xs uppercase tracking-widest font-semibold">{status.original_filename}</p>
                            </div>
                            <button
                                onClick={() => { setStatus(null); setFile(null); }}
                                className="text-xs text-zinc-500 hover:text-white font-bold uppercase tracking-widest transition-colors"
                            >
                                Reset
                            </button>
                        </div>

                        {/* Parsed Data Visualization */}
                        {status.parsed_json && (
                            <div className="space-y-4">
                                {/* Summary Section */}
                                {status.parsed_json.summary && (
                                    <div className="p-4 bg-black/20 rounded-xl border border-white/5">
                                        <p className="text-zinc-500 text-[10px] font-black uppercase tracking-widest mb-2">Neural Summary</p>
                                        <p className="text-zinc-300 text-sm leading-relaxed">
                                            {status.parsed_json.summary}
                                        </p>
                                    </div>
                                )}

                                {/* Skills Matrix */}
                                {status.parsed_json.skills && status.parsed_json.skills.length > 0 && (
                                    <div className="space-y-2">
                                        <p className="text-zinc-500 text-[10px] font-black uppercase tracking-widest">Detected Skills</p>
                                        <div className="flex flex-wrap gap-2">
                                            {status.parsed_json.skills.map((skill: any, index: number) => {
                                                const skillName = typeof skill === 'string' ? skill : skill.skill;
                                                return (
                                                    <span key={index} className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-medium rounded-full border border-emerald-500/20">
                                                        {skillName}
                                                    </span>
                                                );
                                            })}
                                        </div>
                                    </div>
                                )}

                                {/* Experience Snapshot */}
                                {status.parsed_json.experience && status.parsed_json.experience.length > 0 && (
                                    <div className="space-y-2 pt-2">
                                        <p className="text-zinc-500 text-[10px] font-black uppercase tracking-widest">Career Vector</p>
                                        <div className="space-y-2">
                                            {status.parsed_json.experience.slice(0, 2).map((exp: any, i: number) => (
                                                <div key={i} className="flex justify-between items-center text-xs text-zinc-400 border-b border-white/5 pb-1">
                                                    <span className="font-bold text-zinc-300">{exp.role}</span>
                                                    <span>{exp.company}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {!isParsed && (
                    <button
                        onClick={handleUpload}
                        disabled={!file || uploading}
                        className={`w-full py-4 rounded-xl font-black text-sm uppercase tracking-widest transition-all shadow-xl group relative overflow-hidden ${!file || uploading
                            ? 'bg-zinc-900 text-zinc-700 cursor-not-allowed border border-zinc-800'
                            : 'bg-red-600 text-white hover:bg-red-700 active:scale-[0.98] shadow-red-600/20'
                            }`}
                    >
                        <span className="relative z-10 flex items-center justify-center gap-2">
                            {uploading ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                    Processing...
                                </>
                            ) : (
                                <>
                                    <FileCheck className="w-4 h-4" />
                                    Start Neural Analysis
                                </>
                            )}
                        </span>
                    </button>
                )}
            </div>

            {isParsing ? (
                <div className="p-4 bg-red-600/5 border border-red-600/10 rounded-2xl flex gap-4 animate-in fade-in zoom-in duration-500">
                    <div className="p-2 bg-red-600/10 rounded-lg h-fit">
                        <Info className="w-4 h-4 text-red-500" />
                    </div>
                    <div className="space-y-1">
                        <p className="text-xs font-black text-white uppercase tracking-widest">Analysis in Progress</p>
                        <p className="text-[11px] text-zinc-500 leading-relaxed">
                            Our AI engine is currently deconstructing your resume and indexing your skills against mapped roles.
                        </p>
                    </div>
                </div>
            ) : !isParsed && (
                <div className="p-4 bg-zinc-900/40 rounded-2xl flex gap-4 border border-zinc-800/50 group">
                    <div className="p-2 bg-zinc-800 rounded-lg h-fit group-hover:bg-zinc-700 transition-colors">
                        <AlertCircle className="w-4 h-4 text-zinc-500" />
                    </div>
                    <p className="text-[11px] text-zinc-500 leading-relaxed font-medium">
                        For optimal matching, ensure your resume includes clear project descriptions and technical stack details.
                    </p>
                </div>
            )}
        </div>
    );
};

export default ResumeUpload;
