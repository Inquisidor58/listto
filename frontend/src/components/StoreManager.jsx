import { useState, useEffect } from 'react'
import { api } from '../services/api'

const TABS = [
  { key: 'mercado', icon: '🛒', label: 'Mercado' },
  { key: 'online', icon: '📦', label: 'Online' },
]

export default function StoreManager() {
  const [stores, setStores] = useState([])
  const [tab, setTab] = useState('mercado')
  const [newName, setNewName] = useState('')
  const [editing, setEditing] = useState(null)
  const [editName, setEditName] = useState('')

  const load = async () => {
    try { setStores(await api.getStores({ store_type: tab })) } catch { setStores([]) }
  }

  useEffect(() => { load() }, [tab])

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!newName.trim()) return
    await api.createStore(newName.trim(), tab)
    setNewName('')
    load()
  }

  const handleUpdate = async (id) => {
    if (!editName.trim()) return
    await api.updateStore(id, editName.trim(), tab)
    setEditing(null)
    load()
  }

  const handleDelete = async (id) => {
    await api.deleteStore(id)
    load()
  }

  return (
    <div className="manager">
      <h2>Tiendas</h2>

      <div className="list-tabs" style={{ marginBottom: 12 }}>
        {TABS.map((t) => (
          <button
            key={t.key}
            className={`list-tab tab-${t.key} ${tab === t.key ? 'active' : ''}`}
            onClick={() => setTab(t.key)}
          >
            <span className="tab-icon">{t.icon}</span>
            <span className="tab-label">{t.label}</span>
          </button>
        ))}
      </div>

      <form className="manager-form" onSubmit={handleCreate}>
        <input placeholder={`Nueva tienda ${tab === 'online' ? 'online' : ''}...`} value={newName}
          onChange={(e) => setNewName(e.target.value)} />
        <button type="submit" className="btn-primary">Agregar</button>
      </form>

      <ul className="manager-list">
        {stores.map((s) => (
          <li key={s.id}>
            {editing === s.id ? (
              <>
                <input value={editName} onChange={(e) => setEditName(e.target.value)} />
                <div className="manager-actions">
                  <button className="btn-sm" onClick={() => handleUpdate(s.id)}>✓</button>
                  <button className="btn-sm" onClick={() => setEditing(null)}>✕</button>
                </div>
              </>
            ) : (
              <>
                <span>{s.name}</span>
                <div className="manager-actions">
                  <button className="btn-sm" onClick={() => { setEditing(s.id); setEditName(s.name) }}>✎</button>
                  <button className="btn-sm btn-danger" onClick={() => handleDelete(s.id)}>🗑</button>
                </div>
              </>
            )}
          </li>
        ))}
        {stores.length === 0 && <li className="empty">Sin tiendas de {tab} aún</li>}
      </ul>
    </div>
  )
}
