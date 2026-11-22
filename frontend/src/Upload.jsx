import { useState } from 'react'

export default function Upload() {
  const businessId = 'mysuru_clinic_01'
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file to upload.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('business_id', businessId)

    try {
      const res = await fetch('/api/documents/upload', {
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
        // Reset file input element
        const fileInput = document.getElementById('file-input')
        if (fileInput) fileInput.value = ''
      }
    } catch (err) {
      setError(err.message || 'Network error occurred while uploading document.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload Documents</h2>
      <div className="info-banner">
        Business ID: <strong>{businessId}</strong> (Fixed) &bull; Accepted formats: <strong>.pdf, .txt</strong>
      </div>

      <form onSubmit={handleUpload}>
        <div className="form-group">
          <label htmlFor="file-input">Select Document (.pdf or .txt)</label>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => {
              setError(null)
              setFile(e.target.files[0] || null)
            }}
            disabled={loading}
          />
        </div>
        <button type="submit" className="btn" disabled={loading || !file}>
          {loading ? 'Uploading & Chunking...' : 'Upload Document'}
        </button>
      </form>

      {error && (
        <div className="error-box">
          <strong>Upload Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="success-box">
          <p><strong>Document uploaded and indexed successfully!</strong></p>
          <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
            <li><strong>Filename:</strong> {result.filename}</li>
            <li><strong>Document ID:</strong> {result.document_id}</li>
            <li><strong>Chunks:</strong> {result.chunks}</li>
            <li><strong>Characters:</strong> {result.characters}</li>
          </ul>
        </div>
      )}
    </div>
  )
}
