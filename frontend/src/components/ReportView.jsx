// Tiny markdown renderer: headings, bullets, paragraphs, and [text](url) links.
function inline(text) {
  const parts = [];
  const re = /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g;
  let last = 0, m, k = 0;
  while ((m = re.exec(text))) {
    if (m.index > last) parts.push(text.slice(last, m.index));
    parts.push(<a key={k++} href={m[2]} target="_blank" rel="noreferrer">{m[1]}</a>);
    last = re.lastIndex;
  }
  if (last < text.length) parts.push(text.slice(last));
  return parts;
}

export default function ReportView({ report }) {
  const blocks = [];
  let bullets = [];
  const flush = () => {
    if (bullets.length) {
      blocks.push(<ul key={`ul${blocks.length}`}>{bullets.map((b, i) => <li key={i}>{inline(b)}</li>)}</ul>);
      bullets = [];
    }
  };

  report.split("\n").forEach((line, i) => {
    if (line.startsWith("- ")) { bullets.push(line.slice(2)); return; }
    flush();
    if (line.startsWith("# ")) blocks.push(<h2 key={i}>{line.slice(2)}</h2>);
    else if (line.startsWith("## ")) blocks.push(<h3 key={i}>{line.slice(3)}</h3>);
    else if (line.trim()) blocks.push(<p key={i}>{inline(line)}</p>);
  });
  flush();

  function download() {
    const url = URL.createObjectURL(new Blob([report], { type: "text/markdown" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "research-report.md";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="card report">
      <div className="report-actions"><button onClick={download}>Download .md</button></div>
      {blocks}
    </section>
  );
}
