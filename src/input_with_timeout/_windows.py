from __future__ import annotations

import time

from ._console import cout, endl

_DELAY = 0.05
_TAB_SIZE = 4
_CR = "\r"
_LF = "\n"
_BS = "\b"
_SP = " "
_ET = "\x03"  # Ctrl+C
_HT = "\t"


def read(prompt: object, timeout: float) -> str:
    import msvcrt

    cout << prompt
    line = ""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()

            if ch in (_CR, _LF):
                cout << endl
                return line

            if ch == _ET:
                raise KeyboardInterrupt

            if ch == _BS:
                if not line:
                    continue
                char = line[-1]
                line = line[:-1]
                if char == _HT:
                    cout << _BS * _TAB_SIZE
                elif char == _SP:
                    cout << _BS
                else:
                    cout << _BS << _SP << _BS
            elif ch == _HT:
                line += ch
                cout << _SP * _TAB_SIZE
            else:
                line += ch
                cout << ch
        else:
            time.sleep(_DELAY)

    if line:
        width = sum(_TAB_SIZE if char == _HT else 1 for char in line)
        cout << _BS * width << _SP * width << _BS * width
    cout << endl
    raise TimeoutError("Timeout occurred.")
