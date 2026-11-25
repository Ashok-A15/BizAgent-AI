import { useState, useRef, useEffect } from 'react'
import { API_BASE } from './config'

function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const INITIAL_WELCOME = {
  id: 'welcome-1',
  sender: 'bot',
  text: 'Hi! I am BizAgent, your clinic assistant. Ask me about timings, services, or book an appointment.',
  time: formatTime(),
  sources: [],
  action: null,
}

const SUGGESTIONS = [
  'What are the clinic timings?',
  'Book an appointment',
  'What services do you offer?',
]

export default function Chat() {
  const businessId = 'mysuru_clinic_01'
  const [messages, setMessages] = useState([INITIAL_WELCOME])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const sendMessage = async (textToSend) => {
    const query = (textToSend || input).trim()
    if (!query || loading) return

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      time: formatTime(),
    }

    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${API_BASE}/api/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: query,
          business_id: businessId,
        }),
      })

      const data = await res.json()

      if (!res.ok) {
        const errorMsg = data.detail || (typeof data === 'string' ? data : JSON.stringify(data))
        setError(errorMsg)
        setMessages((prev) => [
          ...prev,
          {
            id: `bot-err-${Date.now()}`,
            sender: 'bot',
            text: `⚠️ Error: ${errorMsg}`,
            time: formatTime(),
            sources: [],
            action: 'error',
          },
        ])
      } else {
        const botMsg = {
          id: `bot-${Date.now()}`,
          sender: 'bot',
          text: data.reply || 'No response text received.',
          time: formatTime(),
          sources: data.sources || [],
          action: data.action || null,
          tool_result: data.tool_result || null,
        }
        setMessages((prev) => [...prev, botMsg])
      }
    } catch (err) {
      const netError = err.message || 'Network error occurred while connecting to backend.'
      setError(netError)
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-neterr-${Date.now()}`,
          sender: 'bot',
          text: `⚠️ Network error: ${netError}`,
          time: formatTime(),
          sources: [],
          action: 'error',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-window">
      {/* Chat Topbar */}
      <div className="chat-topbar">
        <div className="chat-partner">
          <div className="chat-partner-avatar">B</div>
          <div>
            <div className="chat-partner-name">Mysuru Clinic Assistant</div>
            <div className="chat-partner-status">
              <span className="status-dot"></span> Online &bull; Ready to help
            </div>
          </div>
        </div>
        <div className="clinic-badge">
          ID: <strong>{businessId}</strong>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`msg-row ${msg.sender}`}>
            {msg.sender === 'bot' && <div className="msg-avatar">B</div>}

            <div className="msg-content">
              <div className={`bubble ${msg.sender}`}>{msg.text}</div>

              {/* Bot Meta: Action Pill & Sources */}
              {msg.sender === 'bot' && (
                <div className="msg-meta">
                  <span>{msg.time}</span>
                  {msg.action && msg.action !== 'answer' && (
                    <span className="action-pill">
                      {msg.action === 'book_appointment' && '📅 Appointment Booked'}
                      {msg.action === 'create_ticket' && '🎫 Ticket Created'}
                      {msg.action === 'save_lead' && '👤 Lead Captured'}
                      {!['book_appointment', 'create_ticket', 'save_lead'].includes(msg.action) && msg.action}
                    </span>
                  )}
                </div>
              )}

              {/* Sources Chips */}
              {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
                <div className="sources-container">
                  {msg.sources.map((s, idx) => {
                    const fname = s.filename || s
                    return (
                      <span key={idx} className="source-chip" title="Grounded Source Document">
                        📄 {fname}
                      </span>
                    )
                  })}
                </div>
              )}

              {/* User Timestamp */}
              {msg.sender === 'user' && (
                <div className="msg-meta">
                  <span>{msg.time}</span>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Animated Typing Indicator */}
        {loading && (
          <div className="msg-row bot">
            <div className="msg-avatar">B</div>
            <div className="typing-box">
              <div className="dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="typing-text">BizAgent is thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Question Chips */}
      <div className="suggestions-bar">
        {SUGGESTIONS.map((sug, idx) => (
          <button
            key={idx}
            type="button"
            className="suggestion-chip"
            onClick={() => sendMessage(sug)}
            disabled={loading}
          >
            💡 {sug}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="chat-input-area">
        <form
          className="chat-form"
          onSubmit={(e) => {
            e.preventDefault()
            sendMessage()
          }}
        >
          <input
            type="text"
            className="chat-input"
            placeholder="Type your message... (e.g., 'What are the clinic timings?')"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            autoFocus
          />
          <button
            type="submit"
            className="send-btn"
            disabled={loading || !input.trim()}
            title="Send Message"
            aria-label="Send"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  )
}
