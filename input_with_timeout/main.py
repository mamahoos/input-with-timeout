from __future__ import annotations

import builtins
import sys
import time
from typing import Any, Callable, Optional, Union

from .console_output import cout, endl

_DELAY = 0.05
_TAB_SIZE = 4
_CR = "\r"
_LF = "\n"
_BS = "\b"
_SP = " "
_ET = "\x03"  # Ctrl+C
_HT = "\t"


def windows_input_with_timeout(prompt: object, timeout: float) -> str:
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


def unix_input_with_timeout(prompt: object, timeout: float) -> str:
    import select

    cout << prompt
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip("\n")
    cout << endl
    raise TimeoutError("Timeout occurred.")


def _resolve_impl() -> Callable[[object, float], str]:
    if sys.platform == "win32":
        return windows_input_with_timeout
    return unix_input_with_timeout


def input_with_timeout(
    prompt: Any = "",
    /,
    timeout: Optional[Union[int, float]] = 20.0,
) -> str:
    """\
    This function prompts the user for input and returns the input if received within the specified `timeout`.
    If the input is not received within the `timeout`, a TimeoutError is raised.

    ### Parameters:
    - prompt (Any): The text to display before waiting for input.
    - timeout (Union[int, float, None]): The maximum time to wait for input. Set to `None` for no `timeout`.

    ### Returns:
    - str: The user input if received within the specified `timeout`.

    ### Raises:
    - TimeoutError: If no input is received within the specified `timeout`.
    - TypeError: If the `timeout` is not an instance of `int`, `float`, or `None`.
    - ValueError: If the `timeout` value is less than or equal to zero.

    ### Usage:
    ```python
        # To get input with a timeout:
        result = input_with_timeout("Please enter your input: ", timeout=15.0)

        # To get input without a timeout:
        result = input_with_timeout("Please enter your input: ", timeout=None)
    ```
    """
    if not isinstance(timeout, (int, float, type(None))):
        raise TypeError(
            f"timeout must be 'int' or 'float' or 'None', not {type(timeout)}."
        )
    if timeout is None:
        return builtins.input(prompt)
    if timeout <= 0:
        raise ValueError(
            f"timeout value must be greater than zero, timeout: {timeout}."
        )

    return _resolve_impl()(prompt, float(timeout))
