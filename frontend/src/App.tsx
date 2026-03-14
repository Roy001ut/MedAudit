import { useEffect, useState } from 'react';
import { useAuthStore } from './store/auth.store';
import api from './services/api';
import Login from './pages/Login';
import Dashboard from './components/Dashboard';

function App() {
  const { token, user, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api.get('/auth/me').then(r => setUser(r.data)).catch(() => logout()).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  return token && user ? <Dashboard /> : <Login />;
}

export default App;
