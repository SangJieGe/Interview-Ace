# Architecture

Interview Ace uses a **dual-agent pipeline** connected via WebSocket.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Electron Frontend                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Transcript   │  │   Answer     │  │     Toolbar          │  │
│  │   Panel       │  │   Panel      │  │  (settings, upload)  │  │
│  └──────┬───────┘  └──────▲───────┘  └──────────────────────┘  │
│         │                  │                                      │
│         └───── WebSocket ──┘                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend (:8000)                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Voice Agent (Agent 2)                    │   │
│  │                                                            │   │
│  │  Audio Input ──→ Silero VAD ──→ Speaker ID ──→ Whisper    │   │
│  │       ▲                            │                │      │   │
│  │       │                            ▼                ▼      │   │
│  │  System Audio     Voice Profile Match?     Transcript     │   │
│  │  + Microphone     (candidate vs other)      Segment       │   │
│  └──────────────────────────────────────────────┬───────────┘   │
│                                                  │               │
│                                                  ▼               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                Knowledge Agent (Agent 1)                   │   │
│  │                                                            │   │
│  │  Question ──→ RAG Search ──→ Context Assembly ──→ LLM     │   │
│  │                    │                              │        │   │
│  │                    ▼                              ▼        │   │
│  │              ChromaDB                        Answer        │   │
│  │              (embeddings)                   + Sources      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    REST API (/api)                         │   │
│  │  - POST /knowledge/upload   (ingest documents)            │   │
│  │  - GET  /knowledge/search   (query RAG index)             │   │
│  │  - POST /voice/profile      (create voice profile)        │   │
│  │  - POST /config/llm         (switch LLM provider)         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Interviewer Asks a Question (Audio → Text)

```
System Audio / Microphone
    │
    ▼
AudioCapture (sounddevice)
    │
    ▼
Voice Activity Detection (Silero VAD)
    │ detects speech segments
    ▼
Speaker Diarization
    │ compares against candidate's voice profile
    │ "interviewer" or "candidate"
    ▼
Speech-to-Text (Whisper)
    │ produces transcript segment
    ▼
WebSocket → Frontend (display transcript)
    │
    ▼
Forward to Knowledge Agent
```

### 2. Candidate Gets an Answer (Text → Answer)

```
Transcribed Question (from Voice Agent)
    │
    ▼
RAG Retrieval (ChromaDB)
    │ embeds query, finds top-k relevant chunks
    │ from: resume, job description, notes
    ▼
Prompt Assembly
    │ system prompt + context chunks + question
    ▼
LLM Call (OpenAI / Anthropic / Google / DeepSeek)
    │ generates concise, professional answer
    ▼
WebSocket → Frontend (display answer)
```

## Directory Structure

```
Interview-Ace/
├── backend/                    # Python (FastAPI)
│   ├── main.py                 # App entry point + lifespan
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   ├── routes.py           # REST endpoints (upload, search, config)
│   │   └── ws_routes.py        # WebSocket endpoint (real-time audio)
│   ├── agents/
│   │   ├── agent1/
│   │   │   └── knowledge_agent.py   # RAG + LLM answer generation
│   │   ├── agent2/
│   │   │   └── voice_agent.py       # Audio capture + VAD + diarization + STT
│   │   └── hermes/                  # Hermes integration (mock interviewer)
│   ├── core/
│   │   ├── config.py           # Settings (pydantic-settings, .env)
│   │   └── audio.py            # Audio capture & VAD utilities
│   ├── models/
│   │   └── schemas.py          # Pydantic models (transcript, answer, session)
│   └── rag/
│       └── retriever.py        # ChromaDB-based RAG engine
│
├── frontend/                   # TypeScript (React + Electron)
│   ├── package.json
│   ├── index.html
│   ├── electron/
│   │   ├── main.js             # Electron main process (overlay window)
│   │   └── preload.js          # Context bridge for IPC
│   └── src/
│       ├── main.tsx            # React entry point
│       ├── App.tsx             # Main app layout
│       ├── index.css           # Global styles (Tailwind)
│       ├── components/
│       │   ├── TranscriptPanel.tsx   # Live transcript display
│       │   ├── AnswerPanel.tsx       # Suggested answer display
│       │   └── Toolbar.tsx           # Bottom control bar
│       └── hooks/
│           └── useWebSocket.ts       # WebSocket connection hook
│
├── scripts/
│   ├── setup_audio.sh          # Linux audio routing setup
│   ├── download_models.sh      # Download ML models (Whisper, VAD, embeddings)
│   └── list_devices.py         # List available audio devices
│
├── docs/
│   └── architecture.md         # This file
│
├── docker-compose.yml          # Docker setup (backend + frontend + chromadb)
├── .env.example                # Environment variables template
├── .gitignore
├── CONTRIBUTING.md
└── README.md                   # Project overview & quick start
```

## Key Technology Decisions

| Component | Choice | Why |
|-----------|--------|-----|
| Backend Framework | FastAPI | Async-native, WebSocket support, auto OpenAPI docs |
| Speech-to-Text | Whisper (OpenAI) | Best accuracy for multilingual interviews |
| Voice Activity Detection | Silero VAD | Lightweight, runs on CPU, good accuracy |
| Speaker Diarization | Embedding comparison | Simple, effective for 2-speaker scenario |
| Vector Database | ChromaDB | Zero-config local deployment, good for prototyping |
| Embedding Model | all-MiniLM-L6-v2 | Fast, good quality, 384 dimensions |
| LLM | Configurable | Supports OpenAI, Anthropic, Google, DeepSeek |
| Frontend | React + Electron | Desktop overlay that floats over video calls |
| Styling | Tailwind CSS | Rapid UI development |
| Real-time Comm | WebSocket | Low-latency bidirectional audio/text streaming |

## Adding a New LLM Provider

1. Add provider config to `backend/core/config.py`
2. Add client initialization in `KnowledgeAgent.initialize()`
3. Add API key to `.env.example`
4. Update `update_llm_config()` in `api/routes.py`

## Adding a New Audio Source

1. Add capture logic in `backend/core/audio.py`
2. Update `AudioCapture.start_capture()` to handle new source
3. Wire into Voice Agent pipeline in `voice_agent.py`
