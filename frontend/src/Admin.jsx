import { useState, useEffect } from 'react'

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
        fetch('/api/admin/tickets'),
        fetch('/api/admin/appointments'),
        fetch('/api/admin/leads'),
        fetch('/api/documents'),
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
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <button onClick={loadData} className="btn btn-secondary" disabled={loading}>
          {loading ? 'Refreshing...' : '🔄 Refresh Data'}
        </button>
      </div>

      {error && (
        <div className="error-box" style={{ marginBottom: '20px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* 1. Appointments Section */}
      <div className="card">
        <h3>Appointments ({appointments.length})</h3>
        {appointments.length === 0 ? (
          <p className="empty-text">No items yet</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Date</th>
                <th>Time</th>
                <th>Service</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((appt) => (
                <tr key={appt.id || appt._id}>
                  <td>{appt.customer_name}</td>
                  <td>{appt.date}</td>
                  <td>{appt.time}</td>
                  <td>{appt.service}</td>
                  <td>
                    <span className="action-badge">{appt.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* 2. Tickets Section */}
      <div className="card">
        <h3>Tickets ({tickets.length})</h3>
        {tickets.length === 0 ? (
          <p className="empty-text">No items yet</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((t) => (
                <tr key={t.id || t._id}>
                  <td>{t.title}</td>
                  <td>
                    <span className="action-badge">{t.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* 3. Leads Section */}
      <div className="card">
        <h3>Leads ({leads.length})</h3>
        {leads.length === 0 ? (
          <p className="empty-text">No items yet</p>
        ) : (
          <table>
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
                  <td>{l.name}</td>
                  <td>{l.phone}</td>
                  <td>{l.interest || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* 4. Documents Section */}
      <div className="card">
        <h3>Documents ({documents.length})</h3>
        {documents.length === 0 ? (
          <p className="empty-text">No items yet</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Chunk Count</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((d) => (
                <tr key={d.document_id || d.id}>
                  <td>{d.filename}</td>
                  <td>{d.chunk_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
