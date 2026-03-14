import { useState } from 'react';
import { useAuthStore } from '../store/auth.store';
import api from '../services/api';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setToken, setUser } = useAuthStore();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const { data } = await api.post('/auth/login', { email: form.email, password: form.password });
        setToken(data.access_token);
        setUser(data.user);
      } else {
        await api.post('/auth/register', { email: form.email, password: form.password, full_name: form.full_name });
        setIsLogin(true);
        setForm({ email: '', password: '', full_name: '' });
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-blue-600 text-center mb-8">MedAudit</h1>
        <form onSubmit={submit} className="space-y-4">
          {error && <div className="bg-red-50 text-red-600 p-3 rounded text-sm">{error}</div>}
          <input type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="w-full px-4 py-2 border rounded" required />
          {!isLogin && <input type="text" placeholder="Full Name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className="w-full px-4 py-2 border rounded" required />}
          <input type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="w-full px-4 py-2 border rounded" required minLength={8} />
          <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 rounded font-semibold hover:bg-blue-700">{isLogin ? 'Login' : 'Register'}</button>
        </form>
        <button onClick={() => { setIsLogin(!isLogin); setError(''); }} className="w-full text-blue-600 mt-4 text-sm">{isLogin ? 'Register' : 'Login'}</button>
      </div>
    </div>
  );
}
