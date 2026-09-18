"""Runtime settings from environment variables, with a minimal .env loader."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE lines from .env without overriding variables already set."""
    p = path or Path(os.environ.get("VOC_ENV_FILE", REPO_ROOT / ".env"))
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.split("#", 1)[0].strip().strip('"').strip("'")
        key = key.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class Settings:
    llm_mode: str  # live | cached | fake
    extract_model: str
    extract_effort: str
    theme_model: str
    theme_effort: str
    ask_model: str
    ask_effort: str
    enable_fallbacks: bool
    concurrency: int
    max_usd: float
    data_dir: Path
    port: int
    seed: int
    months: int
    target_calls: int
    company: str
    provider: str            # the default for both roles, kept for back-compat
    ask_provider: str        # anthropic | openrouter | none  — the live Q&A path
    build_provider: str      # anthropic | openrouter | none  — extraction and theming
    ask_key_present: bool
    build_key_present: bool
    or_ask_model: str
    or_extract_model: str
    or_theme_model: str

    @property
    def api_key_present(self) -> bool:
        """Either role can reach a model. Callers that mean one role should say which."""
        return self.ask_key_present or self.build_key_present

    @property
    def can_call_api(self) -> bool:
        """Build-side: whether extraction and theming may call a model themselves."""
        return self.build_key_present and self.llm_mode != "fake"

    @property
    def can_ask_live(self) -> bool:
        return self.ask_key_present and self.llm_mode != "fake"

    @property
    def live_ask_model(self) -> str:
        return self.or_ask_model if self.ask_provider == "openrouter" else self.ask_model


def _key_for(provider: str) -> bool:
    """Whether the role pointed at this provider can reach a model.

    `none` is a real choice, not a missing value: it says the work is done by build-time agents in
    a session rather than through an API, so an accidental run fails loudly instead of quietly
    spending on a model we deliberately did not pick for it.
    """
    if provider == "none":
        return False
    if provider == "openrouter":
        return bool(os.environ.get("OPENROUTER_API_KEY"))
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv()
    provider = _env("VOC_LLM_PROVIDER", "anthropic").lower()
    # Answering and building are different jobs with different risk: a weaker model writing prose
    # over verified numbers is cheap, the same model reading 10k calls is what we already rejected.
    ask_provider = _env("VOC_ASK_PROVIDER", provider).lower()
    build_provider = _env("VOC_BUILD_PROVIDER", provider).lower()
    data_dir = Path(_env("VOC_DATA_DIR", str(REPO_ROOT / "data")))
    if not data_dir.is_absolute():
        data_dir = REPO_ROOT / data_dir
    return Settings(
        llm_mode=_env("VOC_LLM", "cached"),
        extract_model=_env("VOC_EXTRACT_MODEL", "claude-sonnet-5"),
        extract_effort=_env("VOC_EXTRACT_EFFORT", "medium"),
        theme_model=_env("VOC_THEME_MODEL", "claude-sonnet-5"),
        theme_effort=_env("VOC_THEME_EFFORT", "medium"),
        ask_model=_env("VOC_ASK_MODEL", "claude-opus-5"),
        ask_effort=_env("VOC_ASK_EFFORT", "medium"),
        enable_fallbacks=_env("VOC_ENABLE_FALLBACKS", "1") not in ("0", "false", "no"),
        concurrency=int(_env("VOC_CONCURRENCY", "8")),
        max_usd=float(_env("VOC_MAX_USD", "100")),
        data_dir=data_dir,
        port=int(_env("VOC_PORT", "8000")),
        seed=int(_env("VOC_SEED", "20260911")),
        months=int(_env("VOC_MONTHS", "24")),
        target_calls=int(_env("VOC_TARGET_CALLS", "4000")),
        company=_env("VOC_COMPANY", "JPMORGAN CHASE & CO."),
        provider=provider,
        ask_provider=ask_provider,
        build_provider=build_provider,
        ask_key_present=_key_for(ask_provider),
        build_key_present=_key_for(build_provider),
        or_ask_model=_env("VOC_OR_ASK_MODEL", "google/gemini-3.1-pro-preview"),
        or_extract_model=_env("VOC_OR_EXTRACT_MODEL", "google/gemini-2.5-flash"),
        or_theme_model=_env("VOC_OR_THEME_MODEL", "google/gemini-2.5-flash"),
    )


def reset_settings_cache() -> None:
    get_settings.cache_clear()
