import { useAuthStore } from '../store/auth.store';

export default function Dashboard() {
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-600">MedAudit</h1>
          <div>
            <span className="text-gray-600 mr-4">Welcome, {user?.full_name}</span>
            <button onClick={logout} className="bg-red-600 text-white px-4 py-2 rounded">Logout</button>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
          <p className="text-gray-600">Upload documents to get started</p>
        </div>
      </main>
    </div>
  );
}
