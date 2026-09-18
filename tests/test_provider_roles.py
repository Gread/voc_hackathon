"""Answering and building are configured apart.

The live Q&A agent may use a cheaper provider, because the server recounts every number it prints
from the calls it cites. Reading the corpus is a different job: we already rejected a weaker model
there, so the build role can be pointed at `none` and must then refuse to call anything rather than
quietly spending on the model configured for answering.
"""
from __future__ import annotations

import pytest

from voc.config import get_settings, reset_settings_cache
from voc.llm.client import LLMError, get_client


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch: pytest.MonkeyPatch):
    """get_settings() calls load_dotenv(), so the developer's own .env would decide these tests.
    A deleted variable is the giveaway: .env puts it straight back."""
    monkeypatch.setattr("voc.config.load_dotenv", lambda *a, **k: False)


@pytest.fixture
def roles(monkeypatch: pytest.MonkeyPatch):
    def apply(ask: str, build: str, *, anthropic_key: str = "", openrouter_key: str = ""):
        monkeypatch.setenv("VOC_LLM", "cached")
        monkeypatch.setenv("VOC_ASK_PROVIDER", ask)
        monkeypatch.setenv("VOC_BUILD_PROVIDER", build)
        for name, value in (("ANTHROPIC_API_KEY", anthropic_key), ("ANTHROPIC_AUTH_TOKEN", ""),
                            ("OPENROUTER_API_KEY", openrouter_key)):
            if value:
                monkeypatch.setenv(name, value)
            else:
                monkeypatch.delenv(name, raising=False)
        reset_settings_cache()
        return get_settings()

    yield apply
    reset_settings_cache()


def test_ask_can_go_live_while_build_cannot(roles):
    settings = roles("openrouter", "none", openrouter_key="or-test-key")

    assert settings.can_ask_live is True
    assert settings.can_call_api is False, "build must not inherit the answering provider's key"
    assert settings.live_ask_model == settings.or_ask_model


def test_build_role_refuses_instead_of_falling_back(roles):
    roles("openrouter", "none", openrouter_key="or-test-key")

    with pytest.raises(LLMError) as err:
        get_client(mode="live", role="build")
    assert "build" in str(err.value)


def test_each_role_reads_its_own_key(roles):
    # A key for answering only: building stays dark even though a usable provider exists.
    ask_only = roles("openrouter", "anthropic", openrouter_key="or-test-key")
    assert (ask_only.ask_key_present, ask_only.build_key_present) == (True, False)

    # And the other way round.
    build_only = roles("openrouter", "anthropic", anthropic_key="ant-test-key")
    assert (build_only.ask_key_present, build_only.build_key_present) == (False, True)


def test_roles_fall_back_to_the_single_provider_setting(monkeypatch: pytest.MonkeyPatch):
    """Existing setups that only set VOC_LLM_PROVIDER keep working unchanged."""
    monkeypatch.setenv("VOC_LLM", "cached")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("VOC_LLM_PROVIDER", "openrouter")
    monkeypatch.delenv("VOC_ASK_PROVIDER", raising=False)
    monkeypatch.delenv("VOC_BUILD_PROVIDER", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-test-key")
    reset_settings_cache()
    try:
        settings = get_settings()
        assert settings.ask_provider == "openrouter"
        assert settings.build_provider == "openrouter"
        assert settings.can_ask_live and settings.can_call_api
    finally:
        reset_settings_cache()
