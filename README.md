# JCFits Pattern Studio (MVP)

AI-powered fashion CAD MVP for generating graded sewing patterns from garment images.

## Structure

- `frontend/` React + Tailwind + Three.js UX
- `backend/` FastAPI orchestration API
- `ai-models/` notes for CV model integration
- `pattern-engine/` grading and geometry references
- `exports/` generated output files during local runs

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set API base URL with `VITE_API_BASE_URL` if needed (defaults to `http://localhost:8000`).
