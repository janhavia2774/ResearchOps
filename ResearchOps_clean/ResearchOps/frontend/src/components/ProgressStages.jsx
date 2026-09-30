const STAGES = ["Planning", "Web Research", "Verification", "Analysis", "Report Generation"];

export default function ProgressStages({ stage, loading, failed }) {
  return (
    <section className="card stages">
      {STAGES.map((name, i) => {
        let state = "pending";
        let icon = "○";
        if (i < stage) { state = "done"; icon = "✓"; }
        else if (i === stage && failed) { state = "failed"; icon = "✗"; }
        else if (i === stage && loading) { state = "active"; icon = "●"; }
        return (
          <div key={name} className={`stage ${state}`}>
            <span className="stage-icon">{icon}</span> {name}
          </div>
        );
      })}
    </section>
  );
}
