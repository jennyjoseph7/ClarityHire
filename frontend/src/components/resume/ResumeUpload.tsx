import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, FileCheck, AlertCircle, Info, FileText } from 'lucide-react';

const ResumeUpload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<any>(null);

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
            </div>

            {status ? (
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
            ) : (
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
