"""
Anime dataset loader and preprocessor.

Reads the raw MAL (MyAnimeList) CSV, validates schema,
engineers a ``combined_info`` field for embedding, and
saves the processed output ready for vector ingestion.
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from utils.logger import get_logger
from utils.exceptions import AppException

logger = get_logger(__name__)

_REQUIRED_COLUMNS = {"Name", "Genres", "sypnopsis"}


class AnimeDataLoader:
    """
    Load, validate, and preprocess the anime dataset.

    Parameters
    ----------
    raw_path:
        Path to the original ``anime_with_synopsis.csv``.
    processed_path:
        Destination path for the cleaned, combined CSV.
    """

    def __init__(self, raw_path: str, processed_path: str) -> None:
        self.raw_path = Path(raw_path)
        self.processed_path = Path(processed_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_and_process(self) -> str:
        """
        Run the full ETL pipeline.

        Returns
        -------
        str
            Absolute path to the saved processed CSV.
        """
        try:
            logger.info("Loading raw data from '%s'", self.raw_path)
            df = self._load_raw()

            logger.info("Raw data shape: %s rows × %s cols", *df.shape)
            self._validate(df)

            df = self._clean(df)
            df = self._engineer_features(df)

            self._save(df)
            logger.info(
                "Processed data saved to '%s' (%d rows)", self.processed_path, len(df)
            )
            return str(self.processed_path)

        except AppException:
            raise
        except Exception as exc:
            raise AppException("Data loading / processing failed", exc) from exc

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_raw(self) -> pd.DataFrame:
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw data not found at '{self.raw_path}'")
        return pd.read_csv(self.raw_path, encoding="utf-8", on_bad_lines="skip")

    def _validate(self, df: pd.DataFrame) -> None:
        missing = _REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"CSV is missing required columns: {missing}")

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.dropna(subset=list(_REQUIRED_COLUMNS))
        df = df.drop_duplicates(subset=["Name"])
        logger.info("Dropped %d rows with nulls/duplicates", before - len(df))
        return df.reset_index(drop=True)

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df["combined_info"] = (
            "Title: "
            + df["Name"].str.strip()
            + " | Genres: "
            + df["Genres"].str.strip()
            + " | Synopsis: "
            + df["sypnopsis"].str.strip()
        )
        return df[["combined_info"]]

    def _save(self, df: pd.DataFrame) -> None:
        self.processed_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.processed_path, index=False, encoding="utf-8")
