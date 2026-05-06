"""
Interview Ace — Configuration

Loads settings from environment variables using pydantic-settings.
.env file is auto-loaded from project root.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- LLM ---
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"

    FALLBACK_PROVIDER: str = ""
    FALLBACK_API_KEY: str = ""
    FALLBACK_MODEL: str = ""

    # --- Vector DB ---
    VECTOR_DB: str = "chromadb"

    # --- Audio ---
    AUDIO_DEVICE_INDEX: int = 0
    SAMPLE_RATE: int = 16000
    SILENCE_THRESHOLD: float = 0.01
    SILENCE_DURATION: float = 1.5

    # --- Voice Profile ---
    VOICE_PROFILE_PATH: str = "./data/voice_profile.pkl"

    # --- Server ---
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 3000

    # --- Whisper ---
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"

    # --- Knowledge Base ---
    KNOWLEDGE_BASE_DIR: str = "./data/knowledge_base"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    @property
    def knowledge_base_path(self) -> Path:
        return Path(self.KNOWLEDGE_BASE_DIR)


settings = Settings()
