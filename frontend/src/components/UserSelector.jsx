import { useState } from 'react'
import { api } from '../services/api'

const AVATAR_COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16']

function getAvatarColor(name) {
  let hash = 0
  for (let i = 0; i < (name || '').length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]
}

export default function UserSelector({ users, currentUser, onUserChange, onUsersUpdate }) {
  const [open, setOpen] = useState(false)
  const [alias, setAlias] = useState('')
  const [newName, setNewName] = useState('')

  const displayName = currentUser?.alias || currentUser?.name || 'Usuario'
  const initials = displayName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
  const avatarColor = getAvatarColor(displayName)

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!newName.trim()) return
    const user = await api.createUser(newName.trim())
    onUsersUpdate(await api.getUsers())
    onUserChange(user)
    setNewName('')
    setOpen(false)
  }

  const handleSelect = (user) => {
    onUserChange(user)
    setOpen(false)
  }

  const handleSetAlias = async (e) => {
    e.preventDefault()
    if (!currentUser || !alias.trim()) return
    const updated = await api.updateUserAlias(currentUser.id, alias.trim())
    onUserChange(updated)
    onUsersUpdate(await api.getUsers())
    setAlias('')
  }

  return (
    <div className="user-selector">
      <button className="user-btn" onClick={() => { setOpen(!open); setAlias(currentUser?.alias || '') }}>
        <span className="user-avatar" style={{ background: avatarColor }}>{initials}</span>
      </button>

      {open && (
        <div className="user-dropdown" onClick={(e) => e.stopPropagation()}>
          <div className="dropdown-header">Cambiar usuario</div>

          {users.length > 0 && (
            <ul className="user-list">
              {users.map((u) => (
                <li
                  key={u.id}
                  className={currentUser?.id === u.id ? 'active' : ''}
                  onClick={() => handleSelect(u)}
                >
                  <span className="user-avatar-sm" style={{ background: getAvatarColor(u.alias || u.name) }}>{(u.alias || u.name).split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()}</span>
                  {u.alias || u.name}
                </li>
              ))}
            </ul>
          )}

          <form className="user-form" onSubmit={handleCreate}>
            <input placeholder="Nuevo usuario..." value={newName}
              onChange={(e) => setNewName(e.target.value)} />
            <button type="submit">+</button>
          </form>

          {currentUser && (
            <form className="alias-form" onSubmit={handleSetAlias}>
              <label>Alias (nombre visible)</label>
              <div className="alias-form-row">
                <input placeholder="Tu alias..." value={alias}
                  onChange={(e) => setAlias(e.target.value)} />
                <button type="submit">Guardar</button>
              </div>
            </form>
          )}
        </div>
      )}
    </div>
  )
}
