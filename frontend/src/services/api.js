const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function runResearch(question) {
  let res;
  try {
    res = await fetch(`${API}/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
  } catch {
    throw new Error(`Cannot reach the backend at ${API}. Is FastAPI running?`);
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    let detail = data?.detail;
    if (Array.isArray(detail)) detail = detail.map((d) => d.msg).join("; ");
    throw new Error(detail || `Request failed (${res.status})`);
  }
  return data;
}
