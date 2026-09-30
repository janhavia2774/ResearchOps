import { useEffect, useState } from "react";
import { runResearch } from "./services/api.js";
import ProgressStages from "./components/ProgressStages.jsx";
import TaskList from "./components/TaskList.jsx";
import Findings from "./components/Findings.jsx";
import VerificationPanel from "./components/VerificationPanel.jsx";
import ReportView from "./components/ReportView.jsx";

export default function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState(-1); // 0-4 running, 5 = all done
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // The backend runs the whole pipeline in one request, so the stage
  // indicator advances on an estimated timer while we wait.
  useEffect(() => {
    if (!loading) return;
    const id = setInterval(() => setStage((s) => Math.min(s + 1, 4)), 9000);
    return () => clearInterval(id);
  }, [loading]);

  async function start() {
    setLoading(true);
    setError("");
    setResult(null);
    setStage(0);
    try {
      const data = await runResearch(question.trim());
      setResult(data);
      setStage(5);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <header>
        <h1>ResearchOps AI</h1>
        <p>Autonomous multi-agent research assistant</p>
      </header>

      <section className="card">
        <label htmlFor="q">Research question</label>
        <textarea
          id="q"
          rows={3}
          value={question}
          disabled={loading}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Compare solid-state and lithium-ion batteries for electric vehicles"
        />
        <button onClick={start} disabled={loading || question.trim().length < 10}>
          {loading ? "Researching…" : "Start Research"}
        </button>
        {question.trim().length > 0 && question.trim().length < 10 && (
          <small className="hint">Please enter at least 10 characters.</small>
        )}
      </section>

      {(loading || result || error) && (
        <ProgressStages stage={stage} loading={loading} failed={!!error} />
      )}

      {loading && (
        <div className="card loading">
          <div className="spinner" /> Agents are working. This usually takes 30–90 seconds…
        </div>
      )}

      {error && <div className="card error"><strong>Error:</strong> {error}</div>}

      {result && (
        <>
          <TaskList tasks={result.research_tasks} />
          <Findings findings={result.findings} />
          <VerificationPanel verification={result.verification} />
          <ReportView report={result.final_report} />
        </>
      )}
    </div>
  );
}
