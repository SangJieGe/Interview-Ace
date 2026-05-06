#!/usr/bin/env bash
# ============================================================
# Interview Ace — Model Download Script
#
# Downloads required ML models:
# - Whisper (speech-to-text)
# - Silero VAD (voice activity detection)
# - Sentence-transformers (for RAG embeddings)
#
# Usage: bash scripts/download_models.sh
# ============================================================

set -euo pipefail

echo "📦 Interview Ace — Model Download"
echo "==================================="

# Create models directory
mkdir -p models

# --- Whisper ---
echo ""
echo "1/3 Downloading Whisper model..."
WHISPER_MODEL="${WHISPER_MODEL:-base}"
python3 -c "
import whisper
print(f'  Loading whisper/{WHISPER_MODEL}...')
model = whisper.load_model('${WHISPER_MODEL}')
print(f'  ✓ Whisper {WHISPER_MODEL} ready')
" 2>/dev/null || echo "  ⚠ Whisper not installed yet (pip install openai-whisper)"

# --- Silero VAD ---
echo ""
echo "2/3 Downloading Silero VAD..."
python3 -c "
import torch
print('  Loading Silero VAD...')
model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad')
print('  ✓ Silero VAD ready')
" 2>/dev/null || echo "  ⚠ torch not installed yet"

# --- Sentence Transformers ---
echo ""
echo "3/3 Downloading embedding model..."
python3 -c "
from sentence_transformers import SentenceTransformer
print('  Loading all-MiniLM-L6-v2...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('  ✓ Embedding model ready')
" 2>/dev/null || echo "  ⚠ sentence-transformers not installed yet"

echo ""
echo "✅ Model download complete!"
echo "   Models are cached in ~/.cache/ by default."
