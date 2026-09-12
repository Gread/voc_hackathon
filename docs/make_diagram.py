"""One picture of the whole system, generated from the live index so the numbers cannot drift.

Two reading levels on one spine: above it, what a business reader gets at each step; below it, what
an engineer would want to know. Written to SVG, which PowerPoint, Slides and every browser import.

SVG is the source. docs/voc_architecture.png is the same drawing exported at 2x for anywhere that
will not take vector art; re-export it after changing this file.

Usage: python docs/make_diagram.py [output.svg]
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

W, H = 1760, 940
MARGIN = 56
INK = "#14171C"
PAPER = "#FAFAF7"
MUTED = "#6B7280"
FAINT = "#9AA1AC"
ACCENT = "#C2411F"
POSITIVE = "#2F6F4E"
RULE = "#DEDED6"
CARD = "#FFFFFD"
BAND = "#F1F0E9"
FONT = "'Segoe UI',Inter,system-ui,-apple-system,sans-serif"
MONO = "'Cascadia Mono',Consolas,'SF Mono',monospace"


# --- numbers, read from the index --------------------------------------------------------------

def facts() -> dict:
    meta = json.loads((ROOT / "data/meta.json").read_text(encoding="utf-8"))
    con = sqlite3.connect(ROOT / "data/voc.sqlite")

    def one(sql, params=()):
        return con.execute(sql, params).fetchone()[0]

    head = con.execute(
        "SELECT name, n_calls, n_wordings FROM themes WHERE status='active' ORDER BY n_calls DESC LIMIT 1"
    ).fetchone()
    from voc.agent.tools import READ_TOOLS
    return {
        "calls": meta["n_calls"],
        "statements": meta["n_members"],
        "themes": one("SELECT COUNT(*) FROM themes WHERE status='active'"),
        "quote_rate": meta["qa_quote_verify_rate"],
        "months": meta["months"] if "months" in meta else 24,
        "head_name": head[0], "head_calls": head[1], "head_wordings": head[2],
        "n_tools": len(READ_TOOLS),
        "answers": one("SELECT COUNT(*) FROM answers_cache"),
    }


# --- tiny SVG helpers ----------------------------------------------------------------------------

def esc(t) -> str:
    return escape(str(t))


def text(x, y, s, *, size=14, fill=INK, weight="400", anchor="start", font=FONT, spacing=None,
         opacity=None) -> str:
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    extra += f' opacity="{opacity}"' if opacity else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def wrapped(x, y, s, *, width_chars, size=13, fill=MUTED, weight="400", leading=None,
            anchor="start") -> str:
    """Naive word wrap; the caller sizes the column in characters."""
    leading = leading or size * 1.42
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) > width_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "".join(text(x, y + i * leading, ln, size=size, fill=fill, weight=weight, anchor=anchor)
                   for i, ln in enumerate(lines))


def rect(x, y, w, h, *, fill=CARD, stroke=RULE, rx=8, sw=1, opacity=None) -> str:
    op = f' opacity="{opacity}"' if opacity else ""
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{op}/>'


def line(x1, y1, x2, y2, *, stroke=RULE, sw=1, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def chevron(x, y, *, fill=ACCENT, size=9) -> str:
    """A small right-pointing arrow head, used between stages."""
    return (f'<path d="M{x} {y - size} L{x + size * 1.1} {y} L{x} {y + size}" fill="none" '
            f'stroke="{fill}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


# --- the drawing ----------------------------------------------------------------------------------

def build(f: dict, out: Path) -> Path:
    n = 6
    gap = 22
    col = (W - 2 * MARGIN - (n - 1) * gap) / n
    xs = [MARGIN + i * (col + gap) for i in range(n)]

    spine_y = 430
    above_top = 232          # business cards sit above the spine
    below_top = 528          # engineering cards sit below it

    stages = [
        {"n": "1", "title": "Every contact",
         "lead": f"{f['calls']:,} real contacts over {f['months']} months. Not a sample somebody "
                 f"had time to read.",
         "tech_title": "Corpus",
         "tech": ["public regulator complaints, one bank",
                  "constant 25% monthly sample, fixed seed",
                  "plain files are the source of truth"]},
        {"n": "2", "title": "Read, one by one",
         "lead": "Why they called, what they talked about, how they felt, and the exact words that "
                 "show it.",
         "tech_title": "Extraction",
         "tech": ["one model call per contact, strict schema",
                  "cached by content hash, re-runs are free",
                  f"{f['quote_rate'] * 100:.1f}% of quotes are exact substrings"]},
        {"n": "3", "title": "Group into problems",
         "lead": "Hundreds of people describing one failure in different words become one named "
                 "problem.",
         "tech_title": "Theming",
         "tech": [f"{f['statements']:,} statements to {f['themes']} themes, four passes",
                  "grouped by cause, not by keyword",
                  "0.881 agreement when re-judged blind"]},
        {"n": "4", "title": "Watch it move",
         "lead": "Small but accelerating gets flagged now, not in next quarter's report.",
         "tech_title": "Emerging score",
         "tech": ["last 4 weeks against the 16 before",
                  "Poisson z, minimum support to rank",
                  "precomputed weekly, so you can replay it"]},
        {"n": "5", "title": "Ask in plain words",
         "lead": "“Which issues are growing fastest?” Answered with counts, trends and real quotes.",
         "tech_title": "Agent",
         "tech": [f"{f['n_tools']} read-only tools; it queries, never writes",
                  "live on Claude or Gemini, or a recorded run",
                  "round and time budgets bound each question"]},
        {"n": "6", "title": "Check before showing",
         "lead": "The server recounts every claim from the calls, and greys out what it cannot "
                 "support.",
         "tech_title": "Verifier",
         "tech": ["re-queries the call ids and recounts them",
                  "every figure checked against its source",
                  "unverified quotes dropped, never shown"]},
    ]

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect x="0" y="0" width="{W}" height="6" fill="{ACCENT}"/>']

    # --- header
    p.append(text(MARGIN, 62, "Voice of the Customer Insights", size=30, weight="700"))
    p.append(text(MARGIN, 92, "Every customer contact read, grouped into real problems, and every "
                              "number on screen traceable back to the calls behind it.",
                  size=15, fill=MUTED))

    # --- the payoff, full width so it reads as the headline it is
    p.append(rect(MARGIN, 112, W - 2 * MARGIN, 64, fill="#FBEEE9", stroke="#EBD3C9", rx=10))
    p.append(text(MARGIN + 22, 140, f"{f['head_calls']} contacts  ·  {f['head_wordings']} different "
                                    f"wordings  ·  one problem", size=16, weight="700", fill=ACCENT))
    p.append(text(MARGIN + 22, 162, f"“{f['head_name']}”  —  no keyword rule, tag list or dropdown "
                                    f"would ever group these together.", size=12.5, fill=MUTED))

    # --- the two reading levels, each named just above its own band
    p.append(text(MARGIN, 210, "WHAT THE BUSINESS GETS", size=11.5, weight="700", fill=ACCENT, spacing="1.4"))
    p.append(line(MARGIN + 205, 205, W - MARGIN, 205, stroke=RULE))

    p.append(text(MARGIN, 508, "HOW IT IS BUILT", size=11.5, weight="700", fill=MUTED, spacing="1.4"))
    p.append(line(MARGIN + 140, 503, W - MARGIN, 503, stroke=RULE))

    # --- the spine
    p.append(rect(MARGIN - 8, spine_y - 30, W - 2 * MARGIN + 16, 60, fill=BAND, stroke=None, rx=30))

    for i, st in enumerate(stages):
        x = xs[i]
        cx = x + col / 2

        # numbered node on the spine
        p.append(f'<circle cx="{cx}" cy="{spine_y}" r="21" fill="{ACCENT}"/>')
        p.append(text(cx, spine_y + 6, st["n"], size=17, weight="700", fill="#FFFFFF", anchor="middle"))
        p.append(text(cx, spine_y + 46, st["title"], size=15, weight="700", anchor="middle"))

        if i < n - 1:
            p.append(chevron(x + col + gap / 2 - 5, spine_y))

        # above: the business card
        p.append(rect(x, above_top, col, 148))
        p.append(wrapped(x + 18, above_top + 36, st["lead"], width_chars=26, size=15, fill=INK,
                         leading=25))

        # below: the engineering card
        p.append(rect(x, below_top, col, 226, fill="#F7F6F0"))
        p.append(text(x + 17, below_top + 30, st["tech_title"].upper(), size=10.5, weight="700",
                      fill=ACCENT, spacing="1.1"))
        y = below_top + 58
        for bullet in st["tech"]:
            p.append(f'<circle cx="{x + 21}" cy="{y - 4}" r="2.4" fill="{FAINT}"/>')
            block = wrapped(x + 32, y, bullet, width_chars=29, size=12, fill=MUTED, leading=17)
            p.append(block)
            y += 17 * (len(block.split("<text")) - 1) + 12

    # --- foundation strip
    fy = 790
    p.append(rect(MARGIN, fy, W - 2 * MARGIN, 56, fill="#EFEEE6", stroke=None, rx=10))
    found = [
        ("Files are the truth", "the index is derived, rebuilt in seconds"),
        ("Every model call cached", "a killed run resumes, a re-run costs nothing"),
        ("Runs with no API key", "recorded answers replay; the demo needs no network"),
        ("Model is swappable", "Claude or Gemini; the verifier never changes"),
    ]
    fw = (W - 2 * MARGIN) / len(found)
    for i, (title, sub) in enumerate(found):
        fx = MARGIN + i * fw + 22
        p.append(text(fx, fy + 24, title, size=13, weight="700", fill=INK))
        p.append(text(fx, fy + 43, sub, size=11.5, fill=MUTED))
        if i:
            p.append(line(MARGIN + i * fw, fy + 12, MARGIN + i * fw, fy + 44, stroke="#DAD8CE"))

    # --- closing line
    p.append(text(MARGIN, 892, "Every number on the screen is a link to the real calls behind it.",
                  size=17, weight="700", fill=POSITIVE))
    p.append(text(W - MARGIN, 892, f"{f['answers']} demo questions answered offline  ·  "
                                   f"no synthetic records", size=12.5, fill=FAINT, anchor="end"))

    p.append("</svg>")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(p), encoding="utf-8")
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "voc_architecture.svg"
    path = build(facts(), target)
    print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
