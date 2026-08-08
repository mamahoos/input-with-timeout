"""
## Input with Timeout

Cross-platform `input()` with a timeout. Raises `TimeoutError` when the user
does not respond in time.

Project: https://github.com/mamahoos/python-input-with-timeout
"""

from .main import input_with_timeout
from .__version__ import (
    __author__,
    __author_email__,
    __classifiers__,
    __copyright__,
    __description__,
    __keywords__,
    __license__,
    __platforms__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

__all__ = [
    "input_with_timeout",
    "__title__",
    "__description__",
    "__version__",
    "__version_info__",
    "__author__",
    "__author_email__",
    "__url__",
    "__copyright__",
    "__license__",
    "__keywords__",
    "__platforms__",
    "__classifiers__",
]
