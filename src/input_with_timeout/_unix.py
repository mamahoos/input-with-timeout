from __future__ import annotations

import select
import sys

from ._console import cout, endl


def read(prompt: object, timeout: float) -> str:
    cout << prompt
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip("\n")
    cout << endl
    raise TimeoutError("Timeout occurred.")
