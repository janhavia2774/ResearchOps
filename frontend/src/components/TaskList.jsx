export default function TaskList({ tasks }) {
  return (
    <section className="card">
      <h2>Research Tasks</h2>
      <ol>
        {tasks.map((t) => (
          <li key={t.id}>
            <strong>{t.task}</strong>
            <div className="muted">Search query: {t.search_query}</div>
          </li>
        ))}
      </ol>
    </section>
  );
}
