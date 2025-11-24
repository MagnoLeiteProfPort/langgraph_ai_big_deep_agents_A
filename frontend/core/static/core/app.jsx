const { useState } = React;

function AgentAApp() {
  const [subject, setSubject] = useState("");
  const [country, setCountry] = useState("");
  const [budget, setBudget] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResponse("");

    // ✅ Only SUBJECT is mandatory
    if (!subject.trim()) {
      setError("Please fill in SUBJECT (COUNTRY and BUDGET are optional).");
      return;
    }

    // ✅ BUDGET: optional, but if filled, must be a valid number
    let parsedBudget = null;

    if (budget.trim() === "") {
      // you can either leave it null or set a default:
      // parsedBudget = 5000;
      parsedBudget = null;
    } else {
      parsedBudget = Number(budget);
      if (Number.isNaN(parsedBudget)) {
        setError("Budget must be a valid number (or leave it empty).");
        return;
      }
    }

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8001/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject: subject.trim(),        // required
          country: country.trim() || "",  // optional
          budget: parsedBudget,           // optional, may be null
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(
          `Agent A responded with status ${res.status}: ${text.slice(0, 200)}`
        );
      }

      const data = await res.json();
      setResponse(data.result ?? "");
    } catch (err) {
      console.error(err);
      setError(err.message || "Unexpected error calling Agent A.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="badge">
          <span>🧠</span> <span>Agent A Orchestrator</span>
        </div>
        <h1 className="app-title">AI Agentic Explorer</h1>
        <p className="app-subtitle">
          SUBJECT is required. COUNTRY and BUDGET are optional. Agent A will
          derive an axis of exploration and units of analysis, call Agent B for
          each, and summarize everything for you.
        </p>
      </header>

      {/* Form card */}
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div>
              <div className="field-label">Subject *</div>
              <textarea
                className="textarea"
                rows={3}
                placeholder="e.g. Launching a B2B SaaS product for AI-driven marketing analytics"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
            </div>

            <div>
              <div className="field-label">Country (optional)</div>
              <input
                className="input"
                placeholder="e.g. Switzerland"
                value={country}
                onChange={(e) => setCountry(e.target.value)}
              />
              <div className="chip-row">
                <span className="chip">Context</span>
                <span className="chip">Regulation</span>
                <span className="chip">Market maturity</span>
              </div>
            </div>

            <div>
              <div className="field-label">Budget (optional, USD)</div>
              <input
                className="input"
                type="number"
                inputMode="decimal"
                step="any"
                placeholder="Leave empty or type a number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
              />
              <div className="chip-row">
                <span className="chip">MVP ≤ 60 days</span>
                <span className="chip">Limited capital</span>
              </div>
            </div>
          </div>

          <div className="button-row">
            <button className="button" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <span>⏳</span>
                  <span>Running Agent A...</span>
                </>
              ) : (
                <>
                  <span>🚀</span>
                  <span>Run Agent A</span>
                </>
              )}
            </button>
          </div>

          {error && <div className="error">⚠️ {error}</div>}
        </form>
      </div>

      {/* Response card */}
      <div className="card">
        <div className="response-title">Agent A Response</div>
        {loading && !response && (
          <p className="response-body">Agent A is coordinating the calls...</p>
        )}
        {!loading && !response && !error && (
          <p className="response-empty">
            Results will appear here after you run Agent A.
          </p>
        )}
        {response && <div className="response-body">{response}</div>}
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<AgentAApp />);
