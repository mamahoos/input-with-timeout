"""
## Input with Timeout

Cross-platform `input()` with a timeout. Raises `TimeoutError` when the user
does not respond in time.

Project: https://github.com/mamahoos/python-input-with-timeout
"""

from importlib.metadata import PackageNotFoundError, version

from ._core import input_with_timeout

try:
    __version__ = version("input-with-timeout")
except PackageNotFoundError:  # pragma: no cover - only when package metadata is missing
    __version__ = "0.0.0"

__all__ = [
    "input_with_timeout",
    "__version__",
]
