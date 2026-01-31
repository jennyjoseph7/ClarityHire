import React, { useState } from 'react';
import axios from 'axios';
import { User, Lock, Mail, Rocket, ArrowRight, ShieldCheck, Briefcase } from 'lucide-react';

interface AuthProps {
    onLogin: (token: string) => void;
}

const Auth: React.FC<AuthProps> = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleDemoMode = async () => {
        setLoading(true);
        setError('');
        const demoEmail = 'demo@clarityhire.com';
        const demoPass = 'demo123';

        try {
            const params = new URLSearchParams();
            params.append('username', demoEmail);
            params.append('password', demoPass);

            try {
                const res = await axios.post('http://localhost:8000/api/v1/login', params);
                if (res.data?.access_token) {
                    localStorage.setItem('access_token', res.data.access_token);
                    onLogin(res.data.access_token);
                } else {
                    throw new Error('Access token missing from response');
                }
            } catch (e) {
                // Try to register then login
                await axios.post('http://localhost:8000/api/v1/register', {
                    email: demoEmail,
                    password: demoPass,
                    name: 'Demo User',
                    role: 'recruiter'
                });
                const res = await axios.post('http://localhost:8000/api/v1/login', params);
                if (res.data?.access_token) {
                    localStorage.setItem('access_token', res.data.access_token);
                    onLogin(res.data.access_token);
                } else {
                    throw new Error('Access token missing after registration');
                }
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Demo Mode Unavailable. Check Backend.');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (isLogin) {
                const params = new URLSearchParams();
                params.append('username', email);
                params.append('password', password);
                const res = await axios.post('http://localhost:8000/api/v1/login', params);
                if (res.data?.access_token) {
                    localStorage.setItem('access_token', res.data.access_token);
                    onLogin(res.data.access_token);
                } else {
                    throw new Error('Failed to retrieve access token');
                }
            } else {
                await axios.post('http://localhost:8000/api/v1/register', {
                    email,
                    password,
                    name,
                    role: 'candidate'
                });
                setIsLogin(true);
                alert('Account Created! Please Sign In.');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Authentication failed. Please verify credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen bg-black text-white selection:bg-red-500/30">
            {/* Left Side: Auth Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-[#0a0a0a] z-10">
                <div className="max-w-md w-full space-y-8 animate-in fade-in slide-in-from-left duration-700">
                    <div>
                        <div className="flex items-center gap-2 mb-6">
                            <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center shadow-lg shadow-red-600/20">
                                <Briefcase className="text-white w-6 h-6" />
                            </div>
                            <span className="text-2xl font-black tracking-tighter">CLARITY<span className="text-red-600">HIRE</span></span>
                        </div>
                        <h2 className="text-4xl font-black tracking-tight mb-2">
                            {isLogin ? 'Member Login' : 'Create Account'}
                        </h2>
                        <p className="text-zinc-500 text-sm font-medium">
                            {isLogin ? 'Please fill in your basic info' : 'Join our intelligence-driven platform'}
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {!isLogin && (
                            <div className="relative group">
                                <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest ml-1 mb-1 block group-focus-within:text-red-500 transition-colors">Full Name</label>
                                <div className="relative">
                                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-600 group-focus-within:text-red-500 transition-colors" />
                                    <input
                                        type="text"
                                        required
                                        placeholder="Enter your name"
                                        className="w-full bg-[#111] border border-zinc-800 rounded-xl py-3.5 pl-12 pr-4 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all placeholder:text-zinc-700"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                    />
                                </div>
                            </div>
                        )}

                        <div className="relative group">
                            <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest ml-1 mb-1 block group-focus-within:text-red-500 transition-colors">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-600 group-focus-within:text-red-500 transition-colors" />
                                <input
                                    type="email"
                                    required
                                    placeholder="name@company.com"
                                    className="w-full bg-[#111] border border-zinc-800 rounded-xl py-3.5 pl-12 pr-4 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all placeholder:text-zinc-700"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>
                        </div>

                        <div className="relative group">
                            <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest ml-1 mb-1 block group-focus-within:text-red-500 transition-colors">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-600 group-focus-within:text-red-500 transition-colors" />
                                <input
                                    type="password"
                                    required
                                    placeholder="••••••••"
                                    className="w-full bg-[#111] border border-zinc-800 rounded-xl py-3.5 pl-12 pr-4 focus:outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition-all placeholder:text-zinc-700"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            {isLogin && <div className="mt-2 text-right"><a href="#" className="text-zinc-500 text-xs hover:text-red-500 transition-colors italic">Forgot Password?</a></div>}
                        </div>

                        {error && (
                            <div className="p-3 bg-red-900/20 border border-red-900/30 rounded-lg flex items-center gap-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                                <p className="text-red-400 text-xs font-medium">{error}</p>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-4 rounded-xl transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-red-600/20 uppercase tracking-widest text-sm"
                        >
                            {loading ? 'Processing...' : isLogin ? 'Login' : 'Create Account'}
                        </button>

                        <div className="text-center pt-2">
                            <button
                                type="button"
                                onClick={() => setIsLogin(!isLogin)}
                                className="text-zinc-400 hover:text-white transition-colors text-sm"
                            >
                                {isLogin ? (
                                    <>Don't have an account? <span className="text-red-500 font-bold ml-1 active:scale-95 inline-block">Sign Up</span></>
                                ) : (
                                    <>Already have an account? <span className="text-red-500 font-bold ml-1 active:scale-95 inline-block">Sign In</span></>
                                )}
                            </button>
                        </div>
                    </form>

                    <div className="relative py-4">
                        <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-zinc-800"></div></div>
                        <div className="relative flex justify-center text-[10px] uppercase font-bold tracking-[0.2em]"><span className="bg-[#0a0a0a] px-4 text-zinc-500">or experience now</span></div>
                    </div>

                    <button
                        onClick={handleDemoMode}
                        disabled={loading}
                        className="w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-white font-bold py-4 rounded-xl transition-all active:scale-[0.98] flex items-center justify-center gap-3 group"
                    >
                        <Rocket className="w-5 h-5 text-red-500 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                        <span className="uppercase tracking-widest text-sm">Launch Demo Mode</span>
                    </button>
                </div>
            </div>

            {/* Right Side: Visual Content */}
            <div className="hidden lg:block lg:w-1/2 relative overflow-hidden bg-zinc-900">
                <img
                    src="/auth_bg.png"
                    alt="Background"
                    className="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-60"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-[#0a0a0a]/80" />

                <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-12 animate-in fade-in zoom-in duration-1000 delay-300">
                    <div className="inline-flex items-center px-4 py-2 rounded-full bg-red-600/10 border border-red-600/20 text-red-500 text-xs font-bold uppercase tracking-widest mb-6 backdrop-blur-sm">
                        <ShieldCheck className="w-4 h-4 mr-2" />
                        AI-Powered Intelligence
                    </div>
                    <h1 className="text-6xl font-black leading-tight mb-6">
                        The Future of <br />
                        <span className="text-red-600">Hiring</span> is Here.
                    </h1>
                    <p className="text-zinc-400 text-lg max-w-xl mb-12 leading-relaxed">
                        ClarityHire uses advanced neural processing to match elite talent with world-class opportunities. Simple. Transparent. Powered by Data.
                    </p>

                    <div className="grid grid-cols-3 gap-12 pt-10 border-t border-zinc-500/10 w-full max-w-2xl">
                        <div className="space-y-1">
                            <div className="text-3xl font-black text-white">99%</div>
                            <div className="text-zinc-500 text-[10px] uppercase font-bold tracking-widest">Match Accuracy</div>
                        </div>
                        <div className="space-y-1">
                            <div className="text-3xl font-black text-white">10x</div>
                            <div className="text-zinc-500 text-[10px] uppercase font-bold tracking-widest">Faster Screening</div>
                        </div>
                        <div className="space-y-1">
                            <div className="text-3xl font-black text-white">2.5k+</div>
                            <div className="text-zinc-500 text-[10px] uppercase font-bold tracking-widest">Active Jobs</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Auth;
