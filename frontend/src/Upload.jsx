import { useState, useEffect } from 'react'
import { API_BASE } from './config'

export default function Upload() {
  const businessId = 'mysuru_clinic_01'
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [existingDocs, setExistingDocs] = useState([])

  const fetchDocs = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/documents`)
      if (res.ok) {
        const data = await res.json()
        setExistingDocs(data.documents || [])
      }
    } catch {
      // Ignore background docs fetch error
    }
  }

  useEffect(() => {
    fetchDocs()
  }, [])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a document file (.pdf or .txt).')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('business_id', businessId)

    try {
      const res = await fetch(`${API_BASE}/api/documents/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (!res.ok) {
        const errorMsg = data.detail || (typeof data === 'string' ? data : JSON.stringify(data))
        setError(errorMsg)
      } else {
        setResult(data)
        setFile(null)
        const fileInput = document.getElementById('file-input')
        if (fileInput) fileInput.value = ''
        fetchDocs()
      }
    } catch (err) {
      setError(err.message || 'Network error occurred while uploading document.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-card">
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-main)' }}>
          Knowledge Ingestion
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '4px' }}>
          Upload clinic operating guidelines, policy docs, or FAQs to ground your AI assistant.
        </p>
      </div>

      <form onSubmit={handleUpload}>
        <div
          className="dropzone"
          onClick={() => document.getElementById('file-input').click()}
        >
          <div className="dropzone-icon">📄</div>
          <div className="dropzone-title">
            {file ? file.name : 'Click to select or drag and drop document'}
          </div>
          <div className="dropzone-desc">
            Accepted formats: <strong>.pdf, .txt</strong> &bull; Target Business ID:{' '}
            <strong>{businessId}</strong>
          </div>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.txt"
            style={{ display: 'none' }}
            onChange={(e) => {
              setError(null)
              setResult(null)
              setFile(e.target.files[0] || null)
            }}
            disabled={loading}
          />
        </div>

        {file && (
          <div className="file-selected-box">
            <div>
              <strong>Selected:</strong> {file.name} ({(file.size / 1024).toFixed(1)} KB)
            </div>
            <button
              type="button"
              className="btn-secondary"
              style={{ padding: '4px 10px', fontSize: '12px' }}
              onClick={() => setFile(null)}
              disabled={loading}
            >
              ✕ Remove
            </button>
          </div>
        )}

        <div style={{ marginTop: '20px' }}>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading || !file}
            style={{ width: '100%', padding: '12px', fontSize: '15px' }}
          >
            {loading ? 'Chunking & Indexing Embeddings...' : '🚀 Upload & Index Document'}
          </button>
        </div>
      </form>

      {error && (
        <div className="alert-error">
          <strong>Upload Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="alert-success">
          <strong>✅ Document Indexed Successfully!</strong>
          <div style={{ marginTop: '8px', fontSize: '13.5px', lineHeight: '1.6' }}>
            <div>&bull; <strong>Filename:</strong> {result.filename}</div>
            <div>&bull; <strong>Document ID:</strong> {result.document_id}</div>
            <div>&bull; <strong>Generated Chunks:</strong> {result.chunks}</div>
            <div>&bull; <strong>Characters Indexed:</strong> {result.characters}</div>
          </div>
        </div>
      )}

      {/* Existing documents in collection */}
      {existingDocs.length > 0 && (
        <div style={{ marginTop: '32px', paddingTop: '24px', borderTop: '1px solid var(--border)' }}>
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-main)', marginBottom: '12px' }}>
            Currently Indexed Knowledge ({existingDocs.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {existingDocs.map((doc) => (
              <div
                key={doc.document_id || doc.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '10px 14px',
                  background: '#f8fafc',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '13.5px',
                }}
              >
                <span>📄 <strong>{doc.filename}</strong></span>
                <span className="badge success">{doc.chunk_count} Chunks</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
