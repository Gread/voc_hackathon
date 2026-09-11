"""The data/ directory layout, defined once."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from voc.config import get_settings


@dataclass(frozen=True)
class Paths:
    data_dir: Path

    @property
    def raw(self) -> Path:
        return self.data_dir / "raw"

    @property
    def raw_cfpb(self) -> Path:
        return self.raw / "cfpb"

    @property
    def cache(self) -> Path:
        return self.data_dir / "cache"

    @property
    def cache_extract(self) -> Path:
        return self.cache / "extract"

    @property
    def cache_theme(self) -> Path:
        return self.cache / "theme"

    @property
    def work(self) -> Path:
        return self.data_dir / "work"

    @property
    def calls(self) -> Path:
        return self.data_dir / "calls.jsonl"

    @property
    def extractions(self) -> Path:
        return self.data_dir / "extractions.jsonl"

    @property
    def themes_dir(self) -> Path:
        return self.data_dir / "themes"

    @property
    def registry(self) -> Path:
        return self.themes_dir / "registry.json"

    @property
    def members(self) -> Path:
        return self.themes_dir / "members.jsonl"

    @property
    def merges(self) -> Path:
        return self.themes_dir / "merges.json"

    @property
    def answers(self) -> Path:
        return self.data_dir / "answers"

    @property
    def golden(self) -> Path:
        return self.data_dir / "golden"

    @property
    def meta(self) -> Path:
        return self.data_dir / "meta.json"

    @property
    def profile(self) -> Path:
        return self.data_dir / "profile.json"

    @property
    def sqlite(self) -> Path:
        return self.data_dir / "voc.sqlite"

    def ensure(self) -> "Paths":
        for p in (self.raw_cfpb, self.cache_extract, self.cache_theme, self.work,
                  self.themes_dir, self.answers, self.golden):
            p.mkdir(parents=True, exist_ok=True)
        return self


def get_paths(data_dir: Path | None = None) -> Paths:
    return Paths(data_dir or get_settings().data_dir)
