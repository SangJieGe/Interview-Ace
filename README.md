# Interview Ace 🎙️

AI-powered real-time interview assistant with dual-agent voice recognition and smart Q&A generation.

> **What it does**: Sits as a transparent overlay on top of your video call (Zoom, Teams, Google Meet). Listens to the interviewer's questions in real time, searches your resume and prep materials, and suggests smart answers — all within seconds.

## Features

- 🎤 Real-time voice capture from system audio + microphone
- 🗣️ Speaker diarization — automatically separates interviewer from candidate
- 📝 Live transcription powered by Whisper
- 🧠 RAG-based answer generation using your resume, job description, and notes
- 💡 Multi-LLM support (OpenAI, Anthropic, Google, DeepSeek)
- 🖥️ Electron overlay — transparent, always-on-top, floats over any video call
- ⚡ WebSocket-based — low-latency real-time streaming

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- An LLM API key (OpenAI, Anthropic, etc.)

### 1. Clone & Configure

```bash
git clone https://github.com/SangJieGe/Interview-Ace.git
cd Interview-Ace
cp .env.example .env
# Edit .env with your API keys
```

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Electron Overlay (optional)

```bash
cd frontend
npm run electron:dev
```

### 5. Download ML Models

```bash
bash scripts/download_models.sh
```

## Docker (Alternative)

```bash
docker-compose up --build
```

This starts backend, frontend, and ChromaDB vector store.

## How It Works

```
┌──────────────┐     ┌──────────────────────────────────┐
│  Video Call   │     │         Interview Ace             │
│  (Zoom/Teams) │────▶│                                  │
│               │     │  Voice Agent ──→ Knowledge Agent  │
│  Interviewer  │     │  (listen +      (search +        │
│  asks question│     │   transcribe)    generate answer) │
│               │     │       │                │          │
└──────────────┘     │       ▼                ▼          │
                      │  📝 Transcript   💡 Answer        │
                      │  shown live      shown live       │
                      └──────────────────────────────────┘
```

1. **Voice Agent (Agent 2)** captures audio, detects speech, identifies who's speaking, and transcribes using Whisper
2. **Knowledge Agent (Agent 1)** takes the transcribed question, searches your documents via RAG, and generates a contextual answer using an LLM
3. Both transcript and answer appear in real-time on the overlay

## Configuration

All configuration is via environment variables. See `.env.example` for the full list.

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (`openai`, `anthropic`, `google`, `deepseek`) | `openai` |
| `LLM_API_KEY` | API key for the LLM provider | — |
| `LLM_MODEL` | Model to use | `gpt-4o` |
| `WHISPER_MODEL` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`) | `base` |
| `AUDIO_DEVICE_INDEX` | Audio input device index | `0` |
| `VECTOR_DB` | Vector database (`chromadb`, `pinecone`) | `chromadb` |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, WebSocket |
| Speech-to-Text | OpenAI Whisper |
| Voice Activity Detection | Silero VAD |
| Speaker Diarization | Embedding-based comparison |
| RAG | ChromaDB + sentence-transformers |
| LLM | OpenAI / Anthropic / Google / DeepSeek |
| Frontend | React, TypeScript, Tailwind CSS |
| Desktop | Electron (transparent overlay) |

## Project Structure

```
Interview-Ace/
├── backend/              # Python FastAPI server
│   ├── api/              # REST + WebSocket routes
│   ├── agents/           # Agent 1 (Knowledge) + Agent 2 (Voice)
│   ├── core/             # Config, audio utilities
│   ├── models/           # Pydantic schemas
│   └── rag/              # RAG retrieval engine
├── frontend/             # React + Electron app
│   ├── electron/         # Electron main process
│   └── src/              # React components + hooks
├── scripts/              # Setup & utility scripts
├── docs/                 # Architecture & design docs
└── docker-compose.yml    # Docker deployment
```

See `docs/architecture.md` for the detailed system design.

## Roadmap

- [x] Project scaffolding & architecture
- [ ] Audio capture implementation (system + mic)
- [ ] Voice Activity Detection (Silero VAD integration)
- [ ] Whisper transcription pipeline
- [ ] Speaker diarization (voice profile matching)
- [ ] RAG knowledge base (document upload + retrieval)
- [ ] Knowledge Agent (multi-LLM answer generation)
- [ ] WebSocket real-time streaming
- [ ] Electron overlay UI
- [ ] Voice profile creation wizard
- [ ] Session recording & review
- [ ] Multi-language support

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
