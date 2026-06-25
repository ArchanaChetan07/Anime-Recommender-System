"""
One-time build pipeline.

Run this script once (before starting the app) to:
  1. Load and process the raw anime CSV.
  2. Embed and persist documents to ChromaDB.

Usage
-----
    python -m pipeline.build_pipeline
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path when run directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv()

from config.settings import settings
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreManager
from utils.logger import get_logger
from utils.exceptions import AppException

logger = get_logger(__name__)


def main() -> None:
    logger.info("=" * 60)
    logger.info("Starting build pipeline")
    logger.info("=" * 60)

    try:
        # Step 1 — Data
        logger.info("[1/2] Loading and processing raw data…")
        loader = AnimeDataLoader(
            raw_path=settings.raw_data_path,
            processed_path=settings.processed_data_path,
        )
        processed_path = loader.load_and_process()
        logger.info("[1/2] Done — processed CSV: %s", processed_path)

        # Step 2 — Vector store
        logger.info("[2/2] Building vector store…")
        builder = VectorStoreManager(
            csv_path=processed_path,
            persist_dir=settings.persist_dir,
        )
        builder.build_and_save()
        logger.info("[2/2] Done — index saved to: %s", settings.persist_dir)

        logger.info("=" * 60)
        logger.info("Build pipeline completed successfully ✓")
        logger.info("You can now start the app: streamlit run app/app.py")
        logger.info("=" * 60)

    except AppException as exc:
        logger.error("Build pipeline failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
