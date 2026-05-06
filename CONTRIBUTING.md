# Contributing to Interview Ace

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/SangJieGe/Interview-Ace.git
cd Interview-Ace

# 2. Backend setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # Edit with your API keys

# 3. Frontend setup
cd ../frontend
npm install

# 4. Download ML models
cd ..
bash scripts/download_models.sh
```

## Running Locally

```bash
# Terminal 1: Backend
cd backend && uvicorn backend.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Electron (optional, for overlay mode)
cd frontend && npm run electron:dev
```

## Project Layout

- `backend/` — Python FastAPI server (agents, RAG, API)
- `frontend/` — React + Electron desktop app
- `scripts/` — Setup and utility scripts
- `docs/` — Architecture and design docs

See `docs/architecture.md` for the full system design.

## Code Style

- **Python**: Follow PEP 8, use type hints, docstrings for public functions
- **TypeScript**: Use functional components, hooks, TypeScript strict mode
- **Commits**: Use conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)

## Submitting Changes

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test locally
5. Submit a pull request

## Areas That Need Work

Check the GitHub Issues for tasks labeled `good-first-issue` or `help-wanted`.

Common areas:
- Audio capture implementation (platform-specific)
- Voice diarization accuracy
- Additional LLM provider integrations
- Frontend UI polish
- Documentation improvements
