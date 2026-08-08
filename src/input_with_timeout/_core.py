from __future__ import annotations

import builtins
import sys
from typing import Any, Callable, Optional, Union


def _resolve_impl() -> Callable[[object, float], str]:
    if sys.platform == "win32":
        from ._windows import read
    else:
        from ._unix import read
    return read


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
