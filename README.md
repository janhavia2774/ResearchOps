# ResearchOps AI

Autonomous multi-agent research assistant: question -> planner -> web research (Tavily) -> verification -> analysis (Gemini) -> source-backed report.

## Setup (Python 3.10+, Node 18+)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
```

Edit `.env` and add:

- `GEMINI_API_KEY` (get one at https://aistudio.google.com/apikey)
- `TAVILY_API_KEY` (get one at https://app.tavily.com)

Then start the server:

```bash
uvicorn main:app --reload --port 8000
```

### Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev                     # open http://localhost:5173
```

## Test question

> Compare solid-state batteries and lithium-ion batteries for electric vehicles: current technology status, cost, safety, and commercialization timeline.

## Useful endpoints

- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Saved sessions: http://localhost:8000/history
