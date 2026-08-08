# Input with Timeout

`input_with_timeout` captures user input with a timeout. If the user does not
respond in time, it raises `TimeoutError`.

## Installation

```bash
pip install input-with-timeout
```

or with uv:

```bash
uv add input-with-timeout
```

## Features

- Customizable timeout for user input
- Cross-platform support (Windows and Unix)
- Typed public API (`py.typed`)
- Compatible with Python 3.8+

## Usage

```python
from input_with_timeout import input_with_timeout

try:
    user_input = input_with_timeout("Enter your input: ", timeout=10)
    print(f"Input received: '{user_input}'.")
except TimeoutError:
    print("No input received within the timeout period.")
```

Use `timeout=None` for normal blocking `input()` behavior.

## Contact

https://t.me/mamahoos
