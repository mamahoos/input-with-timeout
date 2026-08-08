from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
from importlib.metadata import metadata

from input_with_timeout import __version__, input_with_timeout


def test_version() -> None:
    assert __version__ == "2.3.0"


def test_homepage_url_from_package_metadata() -> None:
    urls = metadata("input-with-timeout").get_all("Project-URL") or []
    assert any(
        "https://github.com/mamahoos/python-input-with-timeout" in url
        for url in urls
    )


@pytest.mark.parametrize("timeout", ["10", [], {}, object()])
def test_timeout_type_error(timeout: Any) -> None:
    with pytest.raises(TypeError, match="timeout must be"):
        input_with_timeout(timeout=timeout)


@pytest.mark.parametrize("timeout", [0, -1, -0.5])
def test_timeout_value_error(timeout: float) -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        input_with_timeout(timeout=timeout)


def test_timeout_none_uses_builtins_input() -> None:
    with patch("builtins.input", return_value="hello") as mocked:
        assert input_with_timeout("Prompt: ", timeout=None) == "hello"
        mocked.assert_called_once_with("Prompt: ")


def test_unix_timeout_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("input_with_timeout._core.sys.platform", "linux")

    with patch("select.select", return_value=([], [], [])):
        with pytest.raises(TimeoutError, match="Timeout occurred"):
            input_with_timeout("Prompt: ", timeout=0.01)


def test_unix_returns_line(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("input_with_timeout._core.sys.platform", "linux")

    with patch("select.select", return_value=([object()], [], [])):
        with patch("sys.stdin.readline", return_value="answer\n"):
            assert input_with_timeout("Prompt: ", timeout=1) == "answer"
