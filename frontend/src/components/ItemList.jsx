import { useState, useEffect } from 'react'
import { api } from '../services/api'

function extractDomain(url) {
  try { return new URL(url).hostname.replace('www.', '') } catch { return null }
}

const STORE_COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1',
  '#14b8a6', '#a855f7', '#e11d48', '#65a30d', '#ea580c',
]

function getStoreColor(name) {
  let hash = 0
  for (let i = 0; i < (name || '').length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return STORE_COLORS[Math.abs(hash) % STORE_COLORS.length]
}

const TABS = [
  { key: 'otros', icon: '📋', label: 'Otros' },
  { key: 'online', icon: '📦', label: 'Online' },
  { key: 'deseos', icon: '✨', label: 'Deseos' },
]

export default function ItemList({ currentUser }) {
  const [items, setItems] = useState([])
  const [categories, setCategories] = useState([])
  const [stores, setStores] = useState([])
  const [listType, setListType] = useState('otros')
  const [filterCat, setFilterCat] = useState('')
  const [filterStore, setFilterStore] = useState('')
  const [filterChecked, setFilterChecked] = useState('false')
  const [showForm, setShowForm] = useState(false)

  const [form, setForm] = useState({
    name: '', quantity: 1, url: '', category_id: '', store_id: '', notes: '',
  })

  const catMap = Object.fromEntries(categories.map((c) => [c.id, c.name]))
  const storeMap = Object.fromEntries(stores.map((s) => [s.id, s.name]))

  const isOtros = listType === 'otros'
  const isOnline = listType === 'online'
  const isDeseos = listType === 'deseos'
  const tagClass = isOtros ? 'tag-mercado' : isOnline ? 'tag-online' : 'tag-deseos'

  useEffect(() => {
    api.getCategories().then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    api.getStores({ store_type: listType === 'online' ? 'online' : 'mercado' }).then(setStores).catch(() => {})
  }, [listType])

  useEffect(() => {
    loadItems()
  }, [listType, filterCat, filterStore, filterChecked])

  const loadItems = async () => {
    const params = { list_type: listType === 'otros' ? 'mercado' : listType }
    if (filterCat) params.category_id = filterCat
    if (filterStore) params.store_id = filterStore
    if (filterChecked !== '') params.checked = filterChecked === 'true'
    try {
      const data = await api.getItems(params)
      setItems(sortItems(data, listType))
    } catch { setItems([]) }
  }

  const sortItems = (data, type) => {
    if (type !== 'otros') return data
    return [...data].sort((a, b) => {
      const sa = (storeMap[a.store_id] || '').toLowerCase()
      const sb = (storeMap[b.store_id] || '').toLowerCase()
      if (sa !== sb) return sa.localeCompare(sb)
      const ca = (catMap[a.category_id] || '').toLowerCase()
      const cb = (catMap[b.category_id] || '').toLowerCase()
      if (ca !== cb) return ca.localeCompare(cb)
      return a.name.toLowerCase().localeCompare(b.name.toLowerCase())
    })
  }

  const handleToggle = async (id) => {
    await api.toggleItem(id)
    loadItems()
  }

  const handleDelete = async (id) => {
    await api.deleteItem(id)
    loadItems()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const payload = {
      list_type: listType === 'otros' ? 'mercado' : listType,
      name: form.name,
      notes: form.notes || null,
      user_id: currentUser?.id || null,
    }
    if (isOtros) {
      payload.quantity = form.quantity
      payload.category_id = form.category_id || null
      payload.store_id = form.store_id || null
    }
    if (isOnline) {
      payload.url = form.url || null
    }
    await api.createItem(payload)
    setForm({ name: '', quantity: 1, url: '', category_id: '', store_id: '', notes: '' })
    setShowForm(false)
    loadItems()
  }

  return (
    <div className="item-list">
      <div className="list-tabs">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            className={`list-tab tab-${tab.key === 'otros' ? 'mercado' : tab.key} ${listType === tab.key ? 'active' : ''}`}
            onClick={() => { setListType(tab.key); setFilterCat(''); setFilterStore(''); setFilterChecked('false') }}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      <div className="filters">
        {isOtros && (
          <>
            <select value={filterCat} onChange={(e) => setFilterCat(e.target.value)}>
              <option value="">Todas categorías</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <select value={filterStore} onChange={(e) => setFilterStore(e.target.value)}>
              <option value="">Todas tiendas</option>
              {stores.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </>
        )}
        <select value={filterChecked} onChange={(e) => setFilterChecked(e.target.value)}>
          <option value="false">Pendientes</option>
          <option value="">Todos</option>
          <option value="true">Comprados</option>
        </select>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nuevo'}
        </button>
      </div>

      {showForm && (
        <form className="item-form" onSubmit={handleSubmit}>
          <input required placeholder="¿Qué necesitas?" value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })} />

          {isOtros && (
            <input type="number" min="1" placeholder="Cantidad" value={form.quantity}
              onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value) || 1 })} />
          )}

          {isOnline && (
            <input type="url" placeholder="Link del producto..." value={form.url}
              onChange={(e) => setForm({ ...form, url: e.target.value })} />
          )}

          {isOtros && (
            <select value={form.category_id}
              onChange={(e) => setForm({ ...form, category_id: e.target.value })}>
              <option value="">Sin categoría</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          )}

          {(isOtros || isOnline) && (
            <select value={form.store_id}
              onChange={(e) => setForm({ ...form, store_id: e.target.value })}>
              <option value="">{isOtros ? 'Sin tienda' : 'Sin tienda online'}</option>
              {stores.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          )}

          <input placeholder="Notas (opcional)" value={form.notes}
            onChange={(e) => setForm({ ...form, notes: e.target.value })} />
          <button type="submit">Agregar a {TABS.find(t => t.key === listType)?.label}</button>
        </form>
      )}

      <ul className="items">
        {items.map((item) => {
          const domain = item.url ? extractDomain(item.url) : null
          const faviconUrl = domain ? `https://www.google.com/s2/favicons?domain=${domain}&sz=64` : null
          const storeColor = getStoreColor(storeMap[item.store_id])

          return (
          <li key={item.id} className={`item ${item.checked ? 'checked' : ''}`}>
            <input type="checkbox" checked={item.checked}
              onChange={() => handleToggle(item.id)} />
            {(isOnline && (item.image_url || faviconUrl)) && (
              <div className="item-thumb">
                {item.image_url ? (
                  <img src={item.image_url} alt="" className="thumb-img"
                    onError={(e) => { e.target.onerror = null; e.target.src = faviconUrl }} />
                ) : (
                  <img src={faviconUrl} alt="" className="thumb-favicon" />
                )}
              </div>
            )}
            <div className="item-info">
              <span className="item-name">{item.name}</span>
              <span className="item-meta">
                {isOtros && item.quantity > 1 && `×${item.quantity} `}
                {storeMap[item.store_id] && (
                  <span className="item-tag" style={{ background: `${storeColor}1a`, color: storeColor }}>
                    {storeMap[item.store_id]}
                  </span>
                )}
                {isOtros && catMap[item.category_id] && `· ${catMap[item.category_id]} `}
                {item.notes && ` · ${item.notes}`}
              </span>
              {isOnline && item.url && (
                <a href={item.url} target="_blank" rel="noopener noreferrer"
                  className="item-link" onClick={(e) => e.stopPropagation()}>
                  🔗 Ver producto
                </a>
              )}
            </div>
            <button className="btn-delete" onClick={() => handleDelete(item.id)}>✕</button>
          </li>
          )
        })}
        {items.length === 0 && (
          <li className="empty">
            <span className="empty-icon">📭</span>
            No hay nada aquí aún
          </li>
        )}
      </ul>
    </div>
  )
}
