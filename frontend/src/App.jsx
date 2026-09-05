import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function money(value) {
  return `₹${Number(value || 0).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function App() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);

  async function loadMetrics() {
    try {
      const response = await fetch(`${API}/api/metrics/`);
      const data = await response.json();

      setMetrics(data);
    } catch (error) {
      console.error("Failed to load metrics:", error);
    } finally {
      setLoading(false);
    }
  }

  async function executeRecovery(paymentId) {
  setExecuting(true);
  setExecutionResult(null);

  try {
    const response = await fetch(`${API}/api/recover/${paymentId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      setExecutionResult({
        success: false,
        message: data.detail || "Recovery execution failed",
      });
      return;
    }

    setExecutionResult(data);

// Refresh dashboard metrics and audit trail
await loadMetrics();
await loadAuditLogs();
  } catch (error) {
    console.error("Recovery execution failed:", error);

    setExecutionResult({
      success: false,
      message: "Unable to connect to recovery service",
    });
  } finally {
    setExecuting(false);
  }
}

async function loadAuditLogs() {
  try {
    const response = await fetch(`${API}/api/audit`);
    const data = await response.json();

    setAuditLogs(data.logs || []);
  } catch (error) {
    console.error("Failed to load audit logs:", error);
  }
}

  useEffect(() => {
  loadMetrics();
  loadAuditLogs();
}, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="loader"></div>
        <p>Loading RecoverAI...</p>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="error-screen">
        <h2>Unable to connect to RecoverAI</h2>
        <p>Make sure the FastAPI backend is running.</p>

        <button onClick={loadMetrics}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="app">

      <header className="topbar">

        <div className="brand">
          <div className="logo">R</div>

          <div>
            <h1>RecoverAI</h1>
            <span>Revenue Recovery Intelligence</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Agent Online
        </div>

      </header>

      <main className="container">

        <section className="hero">

          <div>
            <p className="eyebrow">
              AI REVENUE RECOVERY
            </p>

            <h2>
              Recover revenue before
              <br />
              it disappears.
            </h2>

            <p className="hero-text">
              RecoverAI detects payment failures, diagnoses
              the likely cause, selects bounded recovery
              actions and maintains an audit trail.
            </p>
          </div>

          <div className="hero-badge">
            <strong>{metrics.total_transactions}</strong>
            <span>At-risk cases</span>
          </div>

        </section>

        <section className="stats">

          <StatCard
            title="Revenue At Risk"
            value={money(metrics.total_at_risk)}
            subtitle="Detected from failed & abandoned payments"
          />

          <StatCard
            title="Recoverable"
            value={money(metrics.recoverable_amount)}
            subtitle="Passed automated policy checks"
          />

          <StatCard
  title="Measured Recovered"
  value={money(metrics.measured_recovered)}
  subtitle="Recorded from executed recovery outcomes"
/>

          <StatCard
  title="Measured Recovery Rate"
  value={`${metrics.measured_recovery_rate}%`}
  subtitle="Measured recovered / revenue at risk"
/>

        </section>

        <section className="grid">

          <div className="panel">

            <div className="panel-header">
              <div>
                <h3>AI Recovery Decisions</h3>
                <p>Agent decisions across the payment batch</p>
              </div>

              <button
                className="refresh"
                onClick={loadMetrics}
              >
                ↻ Refresh
              </button>
            </div>

            <div className="table-wrapper">

              <table>

                <thead>
                  <tr>
                    <th>Payment</th>
                    <th>Amount</th>
                    <th>Risk</th>
                    <th>Diagnosis</th>
                    <th>Action</th>
                    <th>Policy</th>
                  </tr>
                </thead>

                <tbody>

                  {metrics.transactions.map((payment) => (

                    <tr
                      key={payment.payment_id}
                      onClick={() => setSelected(payment)}
                    >

                      <td>
                        <strong>
                          {payment.payment_id}
                        </strong>

                        <small>
                          {payment.customer_id}
                        </small>
                      </td>

                      <td>
                        {money(payment.amount)}
                      </td>

                      <td>
                        <span
                          className={
                            payment.risk_score >= 70
                              ? "risk high"
                              : payment.risk_score >= 40
                              ? "risk medium"
                              : "risk low"
                          }
                        >
                          {payment.risk_score}
                        </span>
                      </td>

                      <td className="diagnosis">
                        {payment.diagnosis}
                      </td>

                      <td>
                        <span className="action">
                          {payment.final_action.replaceAll("_", " ")}
                        </span>
                      </td>

                      <td>
                        {payment.policy_allowed ? (
                          <span className="allowed">
                            ✓ Allowed
                          </span>
                        ) : (
                          <span className="blocked">
                            ! Blocked
                          </span>
                        )}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>


          <aside className="side-column">

            <div className="panel">

              <div className="panel-header">
                <div>
                  <h3>Recovery Actions</h3>
                  <p>Agent intervention breakdown</p>
                </div>
              </div>

              <ActionBar
                name="Payment Reminder"
                value={metrics.action_counts.send_payment_reminder}
                total={metrics.total_transactions}
              />

              <ActionBar
                name="Checkout Reminder"
                value={metrics.action_counts.send_checkout_reminder}
                total={metrics.total_transactions}
              />

              <ActionBar
                name="Payment Retry"
                value={metrics.action_counts.retry_payment}
                total={metrics.total_transactions}
              />

              <ActionBar
                name="Escalated"
                value={metrics.action_counts.escalate}
                total={metrics.total_transactions}
              />

            </div>


            <div className="panel principles">

              <h3>Agent Guardrails</h3>

              <div className="principle">
                <span>✓</span>
                <div>
                  <strong>Bounded actions</strong>
                  <p>
                    Recovery actions follow predefined limits.
                  </p>
                </div>
              </div>

              <div className="principle">
                <span>✓</span>
                <div>
                  <strong>Explainable decisions</strong>
                  <p>
                    Every recommendation has a reason.
                  </p>
                </div>
              </div>

              <div className="principle">
                <span>✓</span>
                <div>
                  <strong>Human escalation</strong>
                  <p>
                    High-value or expired cases are escalated.
                  </p>
                </div>
              </div>

              <div className="principle">
                <span>✓</span>
                <div>
                  <strong>Audit trail</strong>
                  <p>
                    Decisions are recorded for review.
                  </p>
                </div>
              </div>

            </div>

          </aside>

        </section>

        <section className="audit-panel panel">
  <div className="panel-header">
    <div>
      <h3>Recovery Execution Audit Trail</h3>
      <p>Every executed recovery action is recorded for review</p>
    </div>

    <span className="audit-count">
      {auditLogs.length} Executed
    </span>
  </div>

  {auditLogs.length === 0 ? (
    <div className="empty-audit">
      <span>◷</span>
      <p>No recovery actions executed yet.</p>
    </div>
  ) : (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Payment</th>
            <th>Amount</th>
            <th>Risk</th>
            <th>Action</th>
            <th>Policy</th>
            <th>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {auditLogs.map((log, index) => (
            <tr key={`${log.payment_id}-${index}`}>
              <td>
                <strong>{log.payment_id}</strong>
              </td>

              <td>{money(log.amount)}</td>

              <td>
                <span
                  className={
                    log.risk_score >= 70
                      ? "risk high"
                      : log.risk_score >= 40
                      ? "risk medium"
                      : "risk low"
                  }
                >
                  {log.risk_score}
                </span>
              </td>

              <td>
                <span className="action">
                  {log.final_action.replaceAll("_", " ")}
                </span>
              </td>

              <td>
                {log.policy_allowed ? (
                  <span className="allowed">✓ Allowed</span>
                ) : (
                  <span className="blocked">! Blocked</span>
                )}
              </td>

              <td className="audit-time">
                {new Date(log.timestamp).toLocaleString("en-IN")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )}
</section>

      </main>


      {selected && (

        <div
          className="modal-backdrop"
          onClick={() => setSelected(null)}
        >

          <div
            className="modal"
            onClick={(e) => e.stopPropagation()}
          >

            <button
              className="close"
              onClick={() => setSelected(null)}
            >
              ×
            </button>

            <p className="eyebrow">
              AI DECISION TRACE
            </p>

            <h2>{selected.payment_id}</h2>

            <div className="modal-amount">
              {money(selected.amount)}
            </div>

            <div className="decision-row">
              <span>Risk Score</span>
              <strong>{selected.risk_score}/100</strong>
            </div>

            <div className="decision-row">
              <span>Diagnosis</span>
              <strong>{selected.diagnosis}</strong>
            </div>

            <div className="decision-row">
              <span>Recommended Action</span>
              <strong>
                {selected.recommended_action.replaceAll("_", " ")}
              </strong>
            </div>

            <div className="decision-row">
              <span>Policy</span>
              <strong>
                {selected.policy_allowed
                  ? "Allowed"
                  : "Blocked"}
              </strong>
            </div>

            <div className="decision-row">
              <span>Final Action</span>
              <strong>{selected.final_action}</strong>
            </div>

            <div className="policy-box">
              <strong>Policy Reason</strong>
              <p>{selected.policy_reason}</p>
            </div>

            {executionResult ? (
  <div className="execution-result">
    {executionResult.success ? (
      <>
        <div className="execution-success">
          <strong>✓ Recovery Executed</strong>
        </div>

        <div className="execution-details">
          <div>
            <span>Action</span>
            <strong>
              {executionResult.decision.final_action.replaceAll("_", " ")}
            </strong>
          </div>

          <div>
            <span>Outcome</span>
            <strong className="recovered-status">
              {executionResult.outcome?.status === "recovered"
                ? "Recovered"
                : "Not Recovered"}
            </strong>
          </div>

          <div>
            <span>Recovered Amount</span>
            <strong className="recovered-amount">
              {money(
                executionResult.outcome?.recovered_amount || 0
              )}
            </strong>
          </div>
        </div>

        <small>
          Demo recovery outcome recorded in audit trail.
        </small>
      </>
    ) : (
      <>
        <strong>
          ⚠{" "}
          {executionResult.duplicate
            ? "Already Executed"
            : "Execution Failed"}
        </strong>

        <p>{executionResult.message}</p>
      </>
    )}
  </div>
) : (
  <button
    className="execute-btn"
    disabled={executing || !selected.policy_allowed}
    onClick={() => executeRecovery(selected.payment_id)}
  >
    {executing ? "Executing..." : "⚡ Execute Recovery"}
  </button>
)}

          </div>

        </div>

      )}

    </div>
  );
}


function StatCard({ title, value, subtitle }) {
  return (
    <div className="stat-card">
      <span>{title}</span>
      <strong>{value}</strong>
      <small>{subtitle}</small>
    </div>
  );
}


function ActionBar({ name, value, total }) {

  const percentage =
    total > 0
      ? Math.round((value / total) * 100)
      : 0;

  return (
    <div className="action-row">

      <div className="action-info">
        <span>{name}</span>
        <strong>{value}</strong>
      </div>

      <div className="bar">
        <div
          className="bar-fill"
          style={{
            width: `${percentage}%`
          }}
        ></div>
      </div>

      <small>{percentage}%</small>

    </div>
  );
}


export default App;