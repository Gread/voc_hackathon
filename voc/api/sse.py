"""Server-sent event encoding and recorded-trace replay."""
from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Iterable

EVENT_NAMES = ("status", "thinking", "tool_call", "tool_result", "answer_delta", "answer", "error", "done")
REPLAY_SPEED = 0.5
REPLAY_CAP_MS = 400


def encode_event(name: str, payload: dict[str, Any]) -> bytes:
    return f"event: {name}\ndata: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n".encode("utf-8")


def decode_stream(text: str) -> list[tuple[str, dict[str, Any]]]:
    """Parse an SSE body into (name, payload) pairs (tests and the UI mock)."""
    out: list[tuple[str, dict[str, Any]]] = []
    for block in text.split("\n\n"):
        name, data = "", ""
        for line in block.splitlines():
            if line.startswith("event: "):
                name = line[7:].strip()
            elif line.startswith("data: "):
                data = line[6:]
        if name:
            out.append((name, json.loads(data) if data else {}))
    return out


async def replay(trace: Iterable[dict[str, Any]], speed: float = REPLAY_SPEED,
                 cap_ms: int = REPLAY_CAP_MS) -> AsyncIterator[bytes]:
    """Re-emit recorded events with the original gaps scaled and capped."""
    prev = 0
    for ev in trace:
        t = int(ev.get("t_ms", 0) or 0)
        delay = max(0, min(cap_ms, int((t - prev) * speed)))
        prev = t
        if delay:
            await asyncio.sleep(delay / 1000)
        yield encode_event(str(ev.get("name", "status")), dict(ev.get("payload") or {}))
