import { useState } from 'react'
import { API_BASE } from './config'

export default function Chat() {
  const businessId = 'mysuru_clinic_01'
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [response, setResponse] = useState(null)

  const handleSend = async (e) => {
    e.preventDefault()
    if (!message.trim()) return

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch(`${API_BASE}/api/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          business_id: businessId,
        }),
      })

      const data = await res.json()

      if (!res.ok) {
        const errorMsg = data.detail || (typeof data === 'string' ? data : JSON.stringify(data))
        setError(errorMsg)
      } else {
        setResponse(data)
      }
    } catch (err) {
      setError(err.message || 'Network error occurred while contacting backend.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Customer Chat</h2>
      <div className="info-banner">
        Business ID: <strong>{businessId}</strong> (Fixed)
      </div>

      <form onSubmit={handleSend}>
        <div className="form-group">
          <label htmlFor="chat-input">Your Message</label>
          <textarea
            id="chat-input"
            rows={3}
            placeholder="Ask a question or request an action (e.g., 'Book an appointment for Arjun...')"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
          />
        </div>
        <button type="submit" className="btn" disabled={loading || !message.trim()}>
          {loading ? 'Thinking...' : 'Send Message'}
        </button>
      </form>

      {error && (
        <div className="error-box">
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && (
        <div className="reply-box">
          <div className="reply-meta">
            <span>
              Action: <span className="action-badge">{response.action || 'answer'}</span>
            </span>
            {response.sources && response.sources.length > 0 && (
              <div className="chips">
                <span>Sources:</span>
                {response.sources.map((s, idx) => (
                  <span key={idx} className="chip">
                    {s.filename || s}
                  </span>
                ))}
              </div>
            )}
            {response.tool_result && (
              <span>
                Result: <code>{JSON.stringify(response.tool_result)}</code>
              </span>
            )}
          </div>
          <div className="reply-text">{response.reply}</div>
        </div>
      )}
    </div>
  )
}
