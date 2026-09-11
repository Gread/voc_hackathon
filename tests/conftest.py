"""Shared pytest fixtures: an isolated data directory and the fake LLM."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from voc.config import reset_settings_cache


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fresh VOC_DATA_DIR with VOC_LLM=fake; settings cache reset before and after."""
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("VOC_DATA_DIR", str(d))
    monkeypatch.setenv("VOC_LLM", "fake")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    reset_settings_cache()
    yield d
    reset_settings_cache()


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent
