export default function VerificationPanel({ verification: v }) {
  const empty =
    !v.conflicts.length && !v.insufficient_evidence.length && !v.irrelevant_sources.length;
  return (
    <section className="card">
      <h2>
        Verification{" "}
        <span className={`badge ${v.status === "passed" ? "high" : "medium"}`}>
          {v.status === "passed" ? "no issues" : "issues found"}
        </span>
      </h2>
      {v.summary && <p>{v.summary}</p>}
      {empty && <p className="muted">No conflicts, weak evidence, or irrelevant sources detected.</p>}

      {v.conflicts.length > 0 && <h3>Conflicting information</h3>}
      {v.conflicts.map((c, i) => (
        <p key={i}>⚠️ <strong>{c.topic}:</strong> {c.details}</p>
      ))}

      {v.insufficient_evidence.length > 0 && <h3>Insufficient evidence</h3>}
      {v.insufficient_evidence.map((e, i) => (
        <p key={i}>• <strong>{e.task}</strong> — {e.reason}</p>
      ))}

      {v.irrelevant_sources.length > 0 && <h3>Irrelevant sources</h3>}
      {v.irrelevant_sources.map((s, i) => (
        <p key={i}>
          • {s.url ? <a href={s.url} target="_blank" rel="noreferrer">{s.title || s.source_id}</a> : s.source_id} — {s.reason}
        </p>
      ))}
    </section>
  );
}
