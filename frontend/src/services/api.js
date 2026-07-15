const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const error = await res.text().catch(() => res.statusText)
    throw new Error(error)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  getItems: (params = {}) => {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null) qs.set(k, v) })
    return request(`/items?${qs.toString()}`)
  },
  createItem: (data) => request('/items', { method: 'POST', body: JSON.stringify(data) }),
  updateItem: (id, data) => request(`/items/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteItem: (id) => request(`/items/${id}`, { method: 'DELETE' }),
  toggleItem: (id) => request(`/items/${id}/toggle`, { method: 'POST' }),

  getCategories: () => request('/categories'),
  createCategory: (name) => request('/categories', { method: 'POST', body: JSON.stringify({ name }) }),
  updateCategory: (id, name) => request(`/categories/${id}`, { method: 'PUT', body: JSON.stringify({ name }) }),
  deleteCategory: (id) => request(`/categories/${id}`, { method: 'DELETE' }),

  getStores: (params = {}) => {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null) qs.set(k, v) })
    return request(`/stores?${qs.toString()}`)
  },
  createStore: (name, store_type = 'mercado') => request('/stores', { method: 'POST', body: JSON.stringify({ name, store_type }) }),
  updateStore: (id, name, store_type) => request(`/stores/${id}`, { method: 'PUT', body: JSON.stringify({ name, store_type }) }),
  deleteStore: (id) => request(`/stores/${id}`, { method: 'DELETE' }),

  getUsers: () => request('/users'),
  getMe: () => request('/users/me'),
  createUser: (name) => request('/users', { method: 'POST', body: JSON.stringify({ name }) }),
  updateUserAlias: (id, alias) => request(`/users/${id}/alias`, { method: 'PATCH', body: JSON.stringify({ alias }) }),
  deleteUser: (id) => request(`/users/${id}`, { method: 'DELETE' }),

  getExchangeRate: () => request('/exchange/usd-cop'),
}
