const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function detectGarment(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/api/detect`, { method: 'POST', body: formData })
  if (!response.ok) throw new Error('Detection failed')
  return response.json()
}

export async function generatePattern(payload) {
  const response = await fetch(`${API_BASE}/api/patterns/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error('Pattern generation failed')
  return response.json()
}

export async function exportPattern(payload) {
  const response = await fetch(`${API_BASE}/api/patterns/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error('Export failed')
  return response.json()
}
