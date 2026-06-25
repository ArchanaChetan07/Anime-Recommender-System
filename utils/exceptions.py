"""
Custom exception that captures file name and line number automatically.
"""

import sys
import traceback


class AppException(Exception):
    """
    Application-level exception with enriched context.

    Automatically captures the originating file and line number so
    every log entry contains actionable debugging information.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        self.message = message
        self.cause = cause
        self.detail = self._build_detail()
        super().__init__(self.detail)

    def _build_detail(self) -> str:
        _, _, tb = sys.exc_info()
        if tb is not None:
            frame = traceback.extract_tb(tb)[-1]
            return (
                f"{self.message} | "
                f"cause={self.cause!r} | "
                f"file={frame.filename} | "
                f"line={frame.lineno}"
            )
        return f"{self.message} | cause={self.cause!r}"

    def __str__(self) -> str:
        return self.detail
