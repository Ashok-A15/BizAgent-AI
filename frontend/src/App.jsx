import { useState } from 'react'
import Chat from './Chat'
import Upload from './Upload'
import Admin from './Admin'

export default function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="container">
      <header>
        <h1>BizAgent AI</h1>
        <p>Intelligent AI Agent Platform for Small Businesses</p>
        <nav className="tabs">
          <button
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button
            className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            Upload
          </button>
          <button
            className={`tab-btn ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin')}
          >
            Admin
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
