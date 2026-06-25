"""
Application settings and configuration management.

Loads all environment variables with validation and provides
a single `settings` object used throughout the application.
"""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment."""

    # LLM
    groq_api_key: str = field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    model_name: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "llama-3.1-8b-instant"))
    llm_temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0")))

    # Embeddings
    embedding_model: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    )
    huggingface_api_token: str = field(
        default_factory=lambda: os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    )

    # Vector Store
    persist_dir: str = field(default_factory=lambda: os.getenv("CHROMA_PERSIST_DIR", "chroma_db"))
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "1000")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "100")))
    retriever_k: int = field(default_factory=lambda: int(os.getenv("RETRIEVER_K", "5")))

    # Data
    raw_data_path: str = field(
        default_factory=lambda: os.getenv("RAW_DATA_PATH", "data/anime_with_synopsis.csv")
    )
    processed_data_path: str = field(
        default_factory=lambda: os.getenv("PROCESSED_DATA_PATH", "data/anime_processed.csv")
    )

    def validate(self) -> None:
        """Raise ValueError if required secrets are missing."""
        missing = []
        if not self.groq_api_key:
            missing.append("GROQ_API_KEY")
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Copy .env.example to .env and fill in the values."
            )


# Singleton — import this everywhere
settings = Settings()
