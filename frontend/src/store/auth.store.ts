import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User { id: string; email: string; full_name: string; is_active: boolean; }
interface AuthState {
  user: User | null;
  token: string | null;
  setUser: (u: User) => void;
  setToken: (t: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>(
  persist(
    (set) => ({
      user: null,
      token: null,
      setUser: (user) => { set({ user }); localStorage.setItem('user', JSON.stringify(user)); },
      setToken: (token) => { set({ token }); localStorage.setItem('token', token); },
      logout: () => { set({ user: null, token: null }); localStorage.clear(); },
    }),
    { name: 'auth-storage' }
  )
);
