import { useState, useEffect } from 'react'
import { api } from '../services/api'

export default function CategoryManager() {
  const [categories, setCategories] = useState([])
  const [newName, setNewName] = useState('')
  const [editing, setEditing] = useState(null)
  const [editName, setEditName] = useState('')

  const load = async () => {
    try { setCategories(await api.getCategories()) } catch { setCategories([]) }
  }

  useEffect(() => { load() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!newName.trim()) return
    await api.createCategory(newName.trim())
    setNewName('')
    load()
  }

  const handleUpdate = async (id) => {
    if (!editName.trim()) return
    await api.updateCategory(id, editName.trim())
    setEditing(null)
    load()
  }

  const handleDelete = async (id) => {
    await api.deleteCategory(id)
    load()
  }

  return (
    <div className="manager">
      <h2>Categorías</h2>
      <form className="manager-form" onSubmit={handleCreate}>
        <input placeholder="Nueva categoría..." value={newName}
          onChange={(e) => setNewName(e.target.value)} />
        <button type="submit" className="btn-primary">Agregar</button>
      </form>
      <ul className="manager-list">
        {categories.map((c) => (
          <li key={c.id}>
            {editing === c.id ? (
              <>
                <input value={editName} onChange={(e) => setEditName(e.target.value)} />
                <button className="btn-sm" onClick={() => handleUpdate(c.id)}>✓</button>
                <button className="btn-sm" onClick={() => setEditing(null)}>✕</button>
              </>
            ) : (
              <>
                <span>{c.name}</span>
                <div className="manager-actions">
                  <button className="btn-sm" onClick={() => { setEditing(c.id); setEditName(c.name) }}>✎</button>
                  <button className="btn-sm btn-danger" onClick={() => handleDelete(c.id)}>🗑</button>
                </div>
              </>
            )}
          </li>
        ))}
        {categories.length === 0 && <li className="empty">Sin categorías aún</li>}
      </ul>
    </div>
  )
}
