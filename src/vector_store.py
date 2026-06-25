"""
Vector store construction and retrieval.

Builds a persistent ChromaDB collection from the processed anime
CSV using HuggingFace sentence-transformer embeddings.
"""

from __future__ import annotations

from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

from config.settings import settings
from utils.logger import get_logger
from utils.exceptions import AppException

logger = get_logger(__name__)


class VectorStoreManager:
    """
    Build, persist, and load a ChromaDB vector store.

    Parameters
    ----------
    csv_path:
        Path to the processed anime CSV (``combined_info`` column).
    persist_dir:
        Directory where ChromaDB persists its index.
    """

    def __init__(
        self,
        csv_path: str = "",
        persist_dir: str = settings.persist_dir,
    ) -> None:
        self.csv_path = Path(csv_path) if csv_path else None
        self.persist_dir = persist_dir
        self._embedding = self._build_embeddings()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_and_save(self) -> None:
        """Ingest the CSV, embed documents, and persist to disk."""
        if self.csv_path is None or not self.csv_path.exists():
            raise FileNotFoundError(
                f"Processed CSV not found at '{self.csv_path}'. "
                "Run the build pipeline first."
            )
        try:
            logger.info("Loading documents from '%s'", self.csv_path)
            docs = self._load_documents()

            logger.info("Splitting %d documents into chunks…", len(docs))
            chunks = self._split(docs)
            logger.info("Created %d chunks", len(chunks))

            logger.info("Building ChromaDB at '%s'…", self.persist_dir)
            db = Chroma.from_documents(
                chunks, self._embedding, persist_directory=self.persist_dir
            )
            db.persist()
            logger.info("Vector store saved successfully (%d chunks indexed)", len(chunks))

        except AppException:
            raise
        except Exception as exc:
            raise AppException("Failed to build vector store", exc) from exc

    def load(self) -> Chroma:
        """Load an existing persisted ChromaDB collection."""
        if not Path(self.persist_dir).exists():
            raise FileNotFoundError(
                f"No vector store found at '{self.persist_dir}'. "
                "Run `python -m pipeline.build_pipeline` first."
            )
        logger.info("Loading vector store from '%s'", self.persist_dir)
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self._embedding,
        )

    def as_retriever(self) -> VectorStoreRetriever:
        """Return a retriever configured with the project's ``retriever_k``."""
        return self.load().as_retriever(
            search_type="similarity",
            search_kwargs={"k": settings.retriever_k},
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_embeddings(self) -> HuggingFaceEmbeddings:
        logger.info("Initialising embeddings model '%s'", settings.embedding_model)
        return HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def _load_documents(self):
        loader = CSVLoader(
            file_path=str(self.csv_path),
            source_column="combined_info",
            encoding="utf-8",
        )
        return loader.load()

    def _split(self, docs):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " | ", " ", ""],
        )
        return splitter.split_documents(docs)
