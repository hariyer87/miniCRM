import { Navigate, Route, Routes } from 'react-router-dom'
import { useState } from 'react'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import PatientsPage from './pages/PatientsPage'
import ImagingPage from './pages/ImagingPage'
import Layout from './layout/Layout'
import { User } from './types/models'

function App() {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<User | null>(null)

  const handleLogin = (jwt: string, userData: User) => {
    setToken(jwt)
    setUser(userData)
  }

  if (!token) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <Layout user={user} onLogout={() => { setToken(null); setUser(null) }}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/patients" element={<PatientsPage token={token} />} />
        <Route path="/imaging" element={<ImagingPage token={token} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Layout>
  )
}

export default App
