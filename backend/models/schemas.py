"""
Interview Ace — Data Models

Pydantic models for API request/response and internal data structures.
"""

from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    """A single transcribed speech segment."""
    speaker: str  # "interviewer" | "candidate" | "unknown"
    text: str
    confidence: float
    start_time: float
    end_time: float


class AnswerResponse(BaseModel):
    """Knowledge Agent's generated answer."""
    question: str
    answer: str
    confidence: float
    sources: list[str] = []


class VoiceProfile(BaseModel):
    """Candidate's voice profile metadata."""
    name: str
    embedding_path: str
    sample_duration: float  # seconds of audio used to create profile


class InterviewSession(BaseModel):
    """Tracks a live interview session."""
    session_id: str
    status: str  # "active" | "paused" | "ended"
    transcripts: list[TranscriptSegment] = []
    answers: list[AnswerResponse] = []
    started_at: str | None = None
    ended_at: str | None = None
