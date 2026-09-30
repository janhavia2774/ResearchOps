export default function Findings({ findings }) {
  return (
    <section className="card">
      <h2>Findings & Sources</h2>
      {findings.map((f) => (
        <div key={f.id} className="finding">
          <div className="finding-head">
            <strong>{f.task}</strong>
            <span className={`badge ${f.confidence}`}>{f.confidence} confidence</span>
          </div>
          <p>{f.finding}</p>
          {f.sources.map((s) => (
            <div key={s.id} className="source">
              <a href={s.url} target="_blank" rel="noreferrer">
                [{s.id}] {s.title}
              </a>
              <div className="muted">{s.summary}</div>
            </div>
          ))}
        </div>
      ))}
    </section>
  );
}
