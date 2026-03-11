import { useMemo, useState } from 'react'
import Preview3D from './components/Preview3D'
import { detectGarment, exportPattern, generatePattern } from './lib/api'

const templates = ['Luxury Hoodie', 'Tech Jacket', 'Joggers', 'Sweatpants', 'T-Shirt', 'Cargo Pants', 'Leggings', 'Sports Bra', 'Shorts']

const defaultMeasurements = {
  chest: 40,
  waist: 34,
  hip: 40,
  inseam: 31,
  rise: 11,
  shoulder_width: 18,
  sleeve_length: 25,
  garment_length: 28,
  thigh_circumference: 24,
  ankle_opening: 12,
}

export default function App() {
  const [file, setFile] = useState(null)
  const [template, setTemplate] = useState('Luxury Hoodie')
  const [fit, setFit] = useState('regular')
  const [seamAllowance, setSeamAllowance] = useState(0.375)
  const [measurements, setMeasurements] = useState(defaultMeasurements)
  const [detection, setDetection] = useState(null)
  const [pattern, setPattern] = useState(null)
  const [exports, setExports] = useState(null)
  const [isDetecting, setIsDetecting] = useState(false)
  const [detectError, setDetectError] = useState('')

  const payload = useMemo(
    () => ({ garment_type: template, seam_allowance: seamAllowance, fit, measurements }),
    [fit, measurements, seamAllowance, template],
  )

  const handleDetect = async () => {
    if (!file) {
      setDetectError('Please upload a garment image before running AI detection.')
      return
    }

    setIsDetecting(true)
    setDetectError('')
    try {
      const result = await detectGarment(file)
      setDetection(result)
    } catch (error) {
      setDetection(null)
      setDetectError(error instanceof Error ? error.message : 'Detection failed')
    } finally {
      setIsDetecting(false)
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-8 text-zinc-100">
      <div className="mx-auto max-w-7xl space-y-6">
        <header>
          <h1 className="text-4xl font-semibold">JCFits Pattern Studio</h1>
          <p className="text-zinc-400">AI-powered luxury garment pattern generation and grading.</p>
        </header>

        <section className="grid gap-6 md:grid-cols-2">
          <Card title="Upload Garment">
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            <button className="btn disabled:cursor-not-allowed disabled:bg-zinc-600" disabled={isDetecting} onClick={handleDetect}>
              {isDetecting ? 'Detecting...' : 'Run AI Garment Detection'}
            </button>
            {detectError && <p className="rounded-lg border border-rose-600/50 bg-rose-900/20 p-2 text-sm text-rose-300">{detectError}</p>}
            {detection && <pre className="panel">{JSON.stringify(detection, null, 2)}</pre>}
          </Card>

          <Card title="Garment Template">
            <select className="input" value={template} onChange={(e) => setTemplate(e.target.value)}>
              {templates.map((name) => (
                <option key={name}>{name}</option>
              ))}
            </select>
            <div className="grid grid-cols-2 gap-3">
              <label>
                Seam allowance (in)
                <input className="input" type="number" step="0.125" value={seamAllowance} onChange={(e) => setSeamAllowance(Number(e.target.value))} />
              </label>
              <label>
                Fit
                <select className="input" value={fit} onChange={(e) => setFit(e.target.value)}>
                  <option value="slim">Slim</option>
                  <option value="regular">Regular</option>
                  <option value="oversized">Oversized</option>
                </select>
              </label>
            </div>
          </Card>
        </section>

        <Card title="Enter Measurements">
          <div className="grid gap-3 md:grid-cols-5">
            {Object.entries(measurements).map(([key, val]) => (
              <label key={key} className="text-xs uppercase tracking-wide text-zinc-300">
                {key.replace('_', ' ')}
                <input
                  className="input mt-1"
                  type="number"
                  value={val}
                  onChange={(e) => setMeasurements((prev) => ({ ...prev, [key]: Number(e.target.value) }))}
                />
              </label>
            ))}
          </div>
        </Card>

        <section className="grid gap-6 md:grid-cols-2">
          <Card title="Generate + Edit Pattern">
            <div className="flex gap-2">
              <button className="btn" onClick={async () => setPattern(await generatePattern(payload))}>Generate Pattern</button>
              <button className="btn" onClick={async () => setExports(await exportPattern(payload))}>Export Pattern</button>
            </div>
            <p className="text-sm text-zinc-400">Manual editing tools are represented by measurement + fit controls in this MVP.</p>
            {pattern && <pre className="panel">{JSON.stringify(pattern.graded_sizes?.M || [], null, 2)}</pre>}
            {exports && <pre className="panel">{JSON.stringify(exports, null, 2)}</pre>}
          </Card>

          <Card title="Preview Garment (3D)">
            <Preview3D />
          </Card>
        </section>
      </div>
    </main>
  )
}

function Card({ title, children }) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/60 p-4 shadow-xl">
      <h2 className="mb-3 text-xl font-medium">{title}</h2>
      <div className="space-y-3">{children}</div>
    </div>
  )
}
