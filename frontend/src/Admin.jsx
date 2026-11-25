import { useState, useEffect } from 'react'
import { API_BASE } from './config'

export default function Admin() {
  const [tickets, setTickets] = useState([])
  const [appointments, setAppointments] = useState([])
  const [leads, setLeads] = useState([])
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [ticketsRes, apptsRes, leadsRes, docsRes] = await Promise.all([
        fetch(`${API_BASE}/api/admin/tickets`),
        fetch(`${API_BASE}/api/admin/appointments`),
        fetch(`${API_BASE}/api/admin/leads`),
        fetch(`${API_BASE}/api/documents`),
      ])

      const [ticketsData, apptsData, leadsData, docsData] = await Promise.all([
        ticketsRes.json(),
        apptsRes.json(),
        leadsRes.json(),
        docsRes.json(),
      ])

      setTickets(ticketsData.tickets || [])
      setAppointments(apptsData.appointments || [])
      setLeads(leadsData.leads || [])
      setDocuments(docsData.documents || [])
    } catch (err) {
      setError(err.message || 'Failed to fetch admin data from backend.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  return (
    <div>
      {/* Header with Refresh button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-main)' }}>
            Admin Dashboard
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13.5px', marginTop: '2px' }}>
            Real-time business actions, bookings, tickets, and knowledge metrics.
          </p>
        </div>
        <button onClick={loadData} className="btn-secondary" disabled={loading}>
          {loading ? 'Refreshing...' : '🔄 Refresh Data'}
        </button>
      </div>

      {error && (
        <div className="alert-error" style={{ marginBottom: '20px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Metric Counters Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon green">📅</div>
          <div>
            <div className="stat-value">{appointments.length}</div>
            <div className="stat-label">Appointments</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon blue">🎫</div>
          <div>
            <div className="stat-value">{tickets.length}</div>
            <div className="stat-label">Support Tickets</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon amber">👤</div>
          <div>
            <div className="stat-value">{leads.length}</div>
            <div className="stat-label">Captured Leads</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon purple">📄</div>
          <div>
            <div className="stat-value">{documents.length}</div>
            <div className="stat-label">Knowledge Docs</div>
          </div>
        </div>
      </div>

      {/* 1. Appointments Section */}
      <div className="admin-section">
        <h3>📅 Booked Appointments ({appointments.length})</h3>
        {appointments.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>
            No appointments booked yet.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Customer Name</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Service</th>
                  <th>Phone</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((appt) => (
                  <tr key={appt.id || appt._id}>
                    <td><strong>{appt.customer_name}</strong></td>
                    <td>{appt.date}</td>
                    <td>{appt.time}</td>
                    <td>{appt.service}</td>
                    <td>{appt.phone || '—'}</td>
                    <td>
                      <span className="badge success">{appt.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 2. Tickets Section */}
      <div className="admin-section">
        <h3>🎫 Support Tickets ({tickets.length})</h3>
        {tickets.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>
            No tickets created yet.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Customer / Details</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => (
                  <tr key={t.id || t._id}>
                    <td><strong>{t.title}</strong></td>
                    <td>{t.customer_name || t.details || '—'}</td>
                    <td>
                      <span className="badge info">{t.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 3. Leads Section */}
      <div className="admin-section">
        <h3>👤 Captured Customer Leads ({leads.length})</h3>
        {leads.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>
            No leads captured yet.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Interest</th>
                </tr>
              </thead>
              <tbody>
                {leads.map((l) => (
                  <tr key={l.id || l._id}>
                    <td><strong>{l.name}</strong></td>
                    <td>{l.phone}</td>
                    <td>{l.interest || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 4. Documents Section */}
      <div className="admin-section">
        <h3>📄 Knowledge Documents ({documents.length})</h3>
        {documents.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>
            No documents indexed yet.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Document ID</th>
                  <th>Chunk Count</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((d) => (
                  <tr key={d.document_id || d.id}>
                    <td>📄 <strong>{d.filename}</strong></td>
                    <td><code>{d.document_id || d.id}</code></td>
                    <td><span className="badge success">{d.chunk_count} Chunks</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
