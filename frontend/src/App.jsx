import { useState } from 'react'
import Chat from './Chat'
import Upload from './Upload'
import Admin from './Admin'

export default function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="container">
      <header className="app-header">
        <div className="brand-wrapper">
          <div className="brand-icon">B</div>
          <div className="brand-info">
            <h1>
              BizAgent AI
              <span className="status-badge">
                <span className="status-dot"></span> Online
              </span>
            </h1>
            <p>Intelligent AI Agent for Small Businesses</p>
          </div>
        </div>

        <nav className="tabs-nav" aria-label="Main Navigation">
          <button
            type="button"
            className={`tab-pill ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            type="button"
            className={`tab-pill ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            📁 Upload
          </button>
          <button
            type="button"
            className={`tab-pill ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin')}
          >
            📊 Admin
          </button>
        </nav>
      </header>

      <main>
        {activeTab === 'chat' && <Chat />}
        {activeTab === 'upload' && <Upload />}
        {activeTab === 'admin' && <Admin />}
      </main>
    </div>
  )
}
