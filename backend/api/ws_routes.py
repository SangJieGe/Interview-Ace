"""
Interview Ace — WebSocket Routes

Real-time bidirectional communication between frontend and backend.
Handles audio streaming and live Q&A delivery.

Protocol:
  Client → Server:
    - Binary: raw audio chunks (PCM float32)
    - JSON:  {"type": "config", "payload": {...}}
    - JSON:  {"type": "start_listening"}
    - JSON:  {"type": "stop_listening"}

  Server → Client:
    - JSON:  {"type": "transcript", "payload": {"text": "...", "speaker": "interviewer|candidate"}}
    - JSON:  {"type": "answer", "payload": {"question": "...", "answer": "...", "confidence": 0.95}}
    - JSON:  {"type": "status", "payload": {"voice_agent": "...", "knowledge_agent": "..."}}
"""

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

router = APIRouter()


@router.websocket("/ws/interview")
async def interview_ws(websocket: WebSocket):
    """Main WebSocket endpoint for real-time interview assistance.

    Flow:
    1. Client connects and sends audio stream
    2. Voice Agent: audio → VAD → diarization → transcription
    3. Knowledge Agent: transcript → RAG search → LLM answer
    4. Server sends transcript + answer back to client
    """
    await websocket.accept()
    logger.info("🔌 Client connected to interview WebSocket")

    try:
        while True:
            data = await websocket.receive()

            if "bytes" in data:
                # Binary audio data — forward to Voice Agent
                audio_chunk = data["bytes"]
                # TODO: await voice_agent.process_chunk(audio_chunk)
                pass

            elif "text" in data:
                message = json.loads(data["text"])

                if message["type"] == "start_listening":
                    # TODO: Start audio processing pipeline
                    await websocket.send_json({
                        "type": "status",
                        "payload": {"message": "Listening..."},
                    })

                elif message["type"] == "stop_listening":
                    # TODO: Stop audio processing, flush remaining segments
                    await websocket.send_json({
                        "type": "status",
                        "payload": {"message": "Stopped listening."},
                    })

    except WebSocketDisconnect:
        logger.info("🔌 Client disconnected")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        await websocket.close()
