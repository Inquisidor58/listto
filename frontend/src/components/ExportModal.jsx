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

  const grouped = groupBy === 'store' ? groupByStore(items, storeMap, catMap) : groupByCategory(items, storeMap, catMap)

  const text = grouped
    .map((group) => {
      const header = groupBy === 'store' ? `🛒 ${group.name}` : `📂 ${group.name}`
      const lines = group.items.map((item) => {
        let line = `  • ${item.name}`
        if (item.quantity > 1) line += ` ×${item.quantity}`
        if (groupBy === 'store' && item._cat) line += ` (${item._cat})`
        if (groupBy === 'category' && item._store) line += ` (${item._store})`
        if (item.notes) line += ` — ${item.notes}`
        return line
      })
      return `${header}\n${lines.join('\n')}`
    })
    .join('\n\n')

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      textRef.current?.select()
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

function groupByStore(items, storeMap, catMap) {
  const groups = {}
  for (const item of items) {
    const key = item.store_id || '00000000-0000-0000-0000-000000000000'
    const name = storeMap[item.store_id] || 'Sin tienda'
    if (!groups[key]) groups[key] = { name, items: [] }
    groups[key].items.push({ ...item, _cat: catMap[item.category_id] || '' })
  }
  return Object.entries(groups)
    .sort(([a], [b]) => (a === '00000000-0000-0000-0000-000000000000' ? 1 : b === '00000000-0000-0000-0000-000000000000' ? -1 : 0))
    .map(([, v]) => v)
}

function groupByCategory(items, storeMap, catMap) {
  const groups = {}
  for (const item of items) {
    const key = item.category_id || '00000000-0000-0000-0000-000000000000'
    const name = catMap[item.category_id] || 'Sin categoría'
    if (!groups[key]) groups[key] = { name, items: [] }
    groups[key].items.push({ ...item, _store: storeMap[item.store_id] || '' })
  }
  return Object.entries(groups)
    .sort(([a], [b]) => (a === '00000000-0000-0000-0000-000000000000' ? 1 : b === '00000000-0000-0000-0000-000000000000' ? -1 : 0))
    .map(([, v]) => v)
}
