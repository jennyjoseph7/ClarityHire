import { useState, useEffect } from 'react'
import axios from 'axios'
import ResumeUpload from './components/resume/ResumeUpload'
import JobPosting from './components/job/JobPosting'
import JobList from './components/job/JobList'
import Auth from './components/auth/Auth'
import { Briefcase, LogOut, User as UserIcon, LayoutDashboard, Zap } from 'lucide-react'

function App() {
  const [refreshJobs, setRefreshJobs] = useState(false);
  const [activeTab, setActiveTab] = useState<'candidate' | 'recruiter'>('candidate');
  const [token, setToken] = useState<string | null>(() => {
    const saved = localStorage.getItem('access_token');
    return (saved && saved !== 'undefined' && saved !== 'null') ? saved : null;
  });

  // Global Axios Interceptor for 401s
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          localStorage.removeItem('access_token');
          setToken(null);
        }
        return Promise.reject(error);
      }
    );
    return () => axios.interceptors.response.eject(interceptor);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    setToken(null);
  };

  if (!token) {
    return <Auth onLogin={(newToken) => setToken(newToken)} />;
  }

  return (
    <div className="min-h-screen bg-black text-white selection:bg-red-500/30">
      {/* Premium Gradient Background */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_0%,#1a0505_0%,#000000_70%)] pointer-events-none" />

      <div className="relative z-10 p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          {/* Main Header */}
          <header className="flex flex-col lg:flex-row justify-between items-center mb-12 gap-6 bg-zinc-900/50 backdrop-blur-xl p-5 rounded-[2rem] border border-zinc-800/50 shadow-2xl">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-red-600 rounded-2xl flex items-center justify-center shadow-lg shadow-red-600/30">
                <Briefcase className="text-white w-7 h-7" />
              </div>
              <div>
                <h1 className="text-2xl font-black tracking-tighter leading-none">CLARITY<span className="text-red-500">HIRE</span></h1>
                <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em]">Neural Intelligence</span>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-black/40 p-1.5 rounded-2xl border border-zinc-800/50">
              <button
                onClick={() => setActiveTab('candidate')}
                className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${activeTab === 'candidate'
                  ? 'bg-red-600 text-white shadow-lg shadow-red-600/20'
                  : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50'
                  }`}
              >
                <UserIcon className="w-4 h-4" />
                Candidate View
              </button>
              <button
                onClick={() => setActiveTab('recruiter')}
                className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${activeTab === 'recruiter'
                  ? 'bg-red-600 text-white shadow-lg shadow-red-600/20'
                  : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50'
                  }`}
              >
                <LayoutDashboard className="w-4 h-4" />
                Recruiter Dashboard
              </button>
              <div className="w-px h-6 bg-zinc-800 mx-2" />
              <button
                onClick={handleLogout}
                className="p-2.5 rounded-xl text-zinc-500 hover:text-red-500 hover:bg-red-500/10 transition-all group"
                title="Logout"
              >
                <LogOut className="w-5 h-5 group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          </header>

          <main>
            {activeTab === 'candidate' ? (
              <div className="animate-in fade-in slide-in-from-bottom-6 duration-700">
                <div className="text-center mb-16 space-y-4">
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-red-600/10 border border-red-600/20 text-red-500 text-xs font-black uppercase tracking-widest">
                    <Zap className="w-3.5 h-3.5" />
                    AI-Powered Job Matching
                  </div>
                  <h2 className="text-6xl font-black tracking-tight leading-tight">
                    Elevate Your <br />
                    <span className="text-red-600">Career Matrix</span>
                  </h2>
                  <p className="text-zinc-400 text-lg max-w-2xl mx-auto leading-relaxed">
                    Upload your neural-resume profile and let our engine discover the
                    perfect node in the global workforce.
                  </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                  <aside className="lg:col-span-4 xl:col-span-4 sticky top-8">
                    <ResumeUpload />
                  </aside>
                  <section className="lg:col-span-8 xl:col-span-8">
                    <div className="bg-zinc-900/30 backdrop-blur-sm p-1 rounded-[2rem] border border-zinc-800/50 h-full">
                      <JobList refresh={refreshJobs} />
                    </div>
                  </section>
                </div>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto animate-in fade-in slide-in-from-bottom-6 duration-700">
                <div className="text-center mb-12 space-y-2">
                  <h2 className="text-4xl font-black tracking-tight">Post Neural Requisition</h2>
                  <p className="text-zinc-400 font-medium">Define your criteria and let AI find your next elite performer.</p>
                </div>
                <section className="bg-zinc-900/50 backdrop-blur-xl p-1 rounded-[2.5rem] border border-zinc-800/50 shadow-2xl">
                  <JobPosting onJobCreated={() => setRefreshJobs(!refreshJobs)} />
                </section>
              </div>
            )}
          </main>

          <footer className="mt-20 pt-10 border-t border-zinc-900 text-center">
            <p className="text-zinc-600 text-xs font-bold uppercase tracking-widest">
              © 2026 CLARITYHIRE • Powered by Neural Intelligence
            </p>
          </footer>
        </div>
      </div>
    </div>
  )
}

export default App
