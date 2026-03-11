const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function parseApiError(response, fallbackMessage) {
  try {
    const body = await response.json()
    if (body?.detail) return new Error(typeof body.detail === 'string' ? body.detail : fallbackMessage)
  } catch {
    // ignore json parse errors and use fallback
  }
  return new Error(fallbackMessage)
}

export async function detectGarment(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${API_BASE}/api/detect`, { method: 'POST', body: formData })
  if (!response.ok) throw await parseApiError(response, 'Detection failed. Please upload a valid PNG/JPG/WEBP image.')
  return response.json()
}

export async function generatePattern(payload) {
  const response = await fetch(`${API_BASE}/api/patterns/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw await parseApiError(response, 'Pattern generation failed')
  return response.json()
}

export async function exportPattern(payload) {
  const response = await fetch(`${API_BASE}/api/patterns/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw await parseApiError(response, 'Export failed')
  return response.json()
}
