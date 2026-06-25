"""
Anime recommendation engine.

Wraps a LangChain ``RetrievalQA`` chain backed by Groq's LLaMA model
and exposes a clean ``recommend()`` method that returns a typed result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_groq import ChatGroq

from config.settings import settings
from src.prompt_template import ANIME_PROMPT
from utils.logger import get_logger
from utils.exceptions import AppException

logger = get_logger(__name__)


@dataclass
class RecommendationResult:
    """Structured output from the recommendation engine."""

    answer: str
    source_documents: List[Document]

    @property
    def source_titles(self) -> List[str]:
        """Extract anime titles from retrieved source chunks."""
        titles = []
        for doc in self.source_documents:
            content = doc.page_content
            if "Title:" in content:
                title = content.split("Title:")[1].split("|")[0].strip()
                titles.append(title)
        return list(dict.fromkeys(titles))  # preserve order, deduplicate


class AnimeRecommender:
    """
    RAG-based anime recommendation engine.

    Parameters
    ----------
    retriever:
        A LangChain retriever backed by the anime vector store.
    """

    def __init__(self, retriever: VectorStoreRetriever) -> None:
        self._llm = self._build_llm()
        self._chain = self._build_chain(retriever)
        logger.info(
            "AnimeRecommender initialised | model=%s | temperature=%s",
            settings.model_name,
            settings.llm_temperature,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def recommend(self, query: str) -> RecommendationResult:
        """
        Generate anime recommendations for *query*.

        Parameters
        ----------
        query:
            Natural-language preference description from the user.

        Returns
        -------
        RecommendationResult
            Typed result containing the LLM answer and source documents.
        """
        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

        try:
            logger.info("Processing query: %r", query[:120])
            raw = self._chain.invoke({"query": query})
            result = RecommendationResult(
                answer=raw["result"],
                source_documents=raw.get("source_documents", []),
            )
            logger.info(
                "Recommendation generated | sources=%d", len(result.source_documents)
            )
            return result

        except Exception as exc:
            raise AppException("Recommendation generation failed", exc) from exc

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_llm(self) -> ChatGroq:
        return ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.model_name,
            temperature=settings.llm_temperature,
        )

    def _build_chain(self, retriever: VectorStoreRetriever) -> RetrievalQA:
        return RetrievalQA.from_chain_type(
            llm=self._llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": ANIME_PROMPT},
        )
