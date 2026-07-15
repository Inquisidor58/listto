import { useState, useEffect } from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'
import { api } from './services/api'
import UserSelector from './components/UserSelector'
import ItemList from './components/ItemList'
import CategoryManager from './components/CategoryManager'
import StoreManager from './components/StoreManager'
import ExportModal from './components/ExportModal'

function App() {
  const [users, setUsers] = useState([])
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [usdRate, setUsdRate] = useState(null)
  const [showExport, setShowExport] = useState(false)

  useEffect(() => {
    (async () => {
      try {
        const [me, all] = await Promise.all([
          api.getMe(),
          api.getUsers().catch(() => []),
        ])
        setCurrentUser(me)
        setUsers(all)
      } catch {
        const all = await api.getUsers().catch(() => [])
        setUsers(all)
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  useEffect(() => {
    const fetchRate = async () => {
      try {
        const data = await api.getExchangeRate()
        if (data.usd_cop) setUsdRate(data.usd_cop)
      } catch {}
    }
    fetchRate()
    const interval = setInterval(fetchRate, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="app">
      <header className="header">
        <div className="header-top">
          <div className="header-left">
            <h1>ListTo</h1>
          </div>
          <div className="header-right">
            {usdRate && (
              <span className="exchange-rate">
                💵 ${Number(usdRate).toLocaleString('es-CO', { minimumFractionDigits: 2 })}
              </span>
            )}
            <UserSelector
              users={users}
              currentUser={currentUser}
              onUserChange={setCurrentUser}
              onUsersUpdate={setUsers}
            />
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/" end>Inicio</NavLink>
          <NavLink to="/categories">Categorías</NavLink>
          <NavLink to="/stores">Tiendas</NavLink>
          <button className="nav-btn" onClick={() => setShowExport(true)}>Exportar</button>
        </nav>
      </header>

      <main className="main">
        {loading ? (
          <p style={{ textAlign: 'center', color: '#94a3b8', marginTop: 40 }}>Cargando...</p>
        ) : (
          <Routes>
            <Route path="/" element={<ItemList currentUser={currentUser} />} />
            <Route path="/categories" element={<CategoryManager />} />
            <Route path="/stores" element={<StoreManager />} />
          </Routes>
        )}
      </main>

      {showExport && <ExportModal onClose={() => setShowExport(false)} />}
    </div>
  )
}

export default App
