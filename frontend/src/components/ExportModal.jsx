import { useState, useEffect, useRef } from 'react'
import { api } from '../services/api'

export default function ExportModal({ onClose }) {
  const [items, setItems] = useState([])
  const [stores, setStores] = useState([])
  const [categories, setCategories] = useState([])
  const [groupBy, setGroupBy] = useState('store')
  const textRef = useRef(null)

  const storeMap = Object.fromEntries(stores.map((s) => [s.id, s.name]))
  const catMap = Object.fromEntries(categories.map((c) => [c.id, c.name]))

  useEffect(() => {
    Promise.all([
      api.getItems({ list_type: 'mercado', checked: false }).catch(() => []),
      api.getStores({ store_type: 'mercado' }).catch(() => []),
      api.getCategories().catch(() => []),
    ]).then(([itemData, storeData, catData]) => {
      setItems(itemData)
      setStores(storeData)
      setCategories(catData)
    })
  }, [])

  const groups = buildGroups(items, groupBy, storeMap, catMap)
  const text = formatText(groups)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
    } catch {
      if (textRef.current) {
        textRef.current.select()
        document.execCommand('copy')
      }
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>📋 Exportar lista</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-options">
          <label>Agrupar por:</label>
          <select value={groupBy} onChange={(e) => setGroupBy(e.target.value)}>
            <option value="store">Tienda</option>
            <option value="category">Categoría</option>
          </select>
        </div>

        {items.length === 0 ? (
          <p className="modal-empty">No hay items pendientes</p>
        ) : (
          <>
            <textarea ref={textRef} className="modal-text" readOnly value={text} rows={12} />
            <button className="btn-primary" onClick={handleCopy}>
              📋 Copiar al portapapeles
            </button>
          </>
        )}
      </div>
    </div>
  )
}

const ICONS = { store: '🛒', category: '📂' }

function buildGroups(items, groupBy, storeMap, catMap) {
  const groups = {}
  for (const item of items) {
    const key = groupBy === 'store' ? (item.store_id || 'sin') : (item.category_id || 'sin')
    const name = groupBy === 'store'
      ? (storeMap[item.store_id] || '')
      : (catMap[item.category_id] || '')
    if (!name) continue
    if (!groups[key]) groups[key] = { name, items: [] }
    groups[key].items.push(item)
  }
  return Object.values(groups).sort((a, b) => a.name.localeCompare(b.name))
}

function formatText(groups) {
  return groups.map((g) => {
    const lines = g.items.map((item) => {
      let line = `  • ${item.name}`
      if (item.quantity > 1) line += ` ×${item.quantity}`
      return line
    })
    return `${g.name}\n${lines.join('\n')}`
  }).join('\n\n')
}
