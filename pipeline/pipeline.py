"""
Anime recommendation pipeline.

Composes the vector store and recommender into a single
injectable, cache-friendly object used by the Streamlit app.
"""

from __future__ import annotations

from src.vector_store import VectorStoreManager
from src.recommender import AnimeRecommender, RecommendationResult
from config.settings import settings
from utils.logger import get_logger
from utils.exceptions import AppException

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    """
    End-to-end recommendation pipeline.

    Initialises the vector store retriever and recommendation engine
    once, then serves queries via :py:meth:`recommend`.
    """

    def __init__(self, persist_dir: str = settings.persist_dir) -> None:
        try:
            settings.validate()
            logger.info("Initialising AnimeRecommendationPipeline…")

            store = VectorStoreManager(persist_dir=persist_dir)
            retriever = store.as_retriever()
            self._recommender = AnimeRecommender(retriever)

            logger.info("Pipeline ready.")
        except Exception as exc:
            logger.exception("Pipeline initialisation failed: %s", exc)
            raise AppException("Failed to initialise the recommendation pipeline", exc) from exc

    def recommend(self, query: str) -> RecommendationResult:
        """
        Run the full RAG pipeline for *query*.

        Parameters
        ----------
        query:
            User's natural-language preference description.
        """
        try:
            return self._recommender.recommend(query)
        except Exception as exc:
            logger.error("Pipeline.recommend failed: %s", exc)
            raise AppException("Recommendation failed", exc) from exc
