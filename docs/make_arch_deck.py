"""Build the architecture deck from the live code and index, so no slide can drift from the system.

Usage: python docs/make_arch_deck.py [output.pptx]
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_deck import (ACCENT, BODY_W, H, INK, MARGIN, MUTED, PAPER, POSITIVE, RULE, W, blank,  # noqa: E402
                       bullets, footer, heading, para, quote_card, rule, stat_row, table, textbox)

ROOT = Path(__file__).resolve().parent.parent
CODE_SUFFIXES = (".py", ".js", ".css", ".html")

# Slide copy: the code's own descriptions are written for the model and are far too long for a table
# cell. The tool NAMES still come from TOOL_SPECS, and a tool without a line here fails the build, so
# this can go stale in wording but never in coverage.
TOOL_GLOSS = {
    "get_overview": "Totals, volume by month, top reasons and themes, the sentiment split",
    "contact_reasons": "Reasons ranked, with change on the previous period and the customer's words",
    "list_themes": "Themes ranked by calls, negative mass, emerging score or wordings",
    "theme_detail": "One theme in full: definition, cause, every distinct wording, its weekly series",
    "theme_trend": "Weekly or monthly series for up to six themes or reasons",
    "emerging_themes": "What is new, emerging, growing or fading at a chosen as-of week",
    "sentiment_drivers": "What drives sentiment, with the specific triggers and two verified quotes",
    "breakdown": "One entity by product, channel, region or segment, with lift and suppression",
    "compare": "Two filtered scopes side by side, and what differs most between them",
    "get_quotes": "Verified verbatim statements, spread across months and products",
    "search_calls": "Full-text search over the contact texts and the extracted statements",
    "get_call": "One contact in full: text, metadata, everything extracted, its themes",
    "submit_answer": "The final answer: claims, quotes, charts, caveats and follow-ups",
}


# --- facts, read from the code and the index --------------------------------------------------

def _gloss(name: str) -> str:
    """A tool with no slide copy is a build failure, not a silently missing row."""
    try:
        return TOOL_GLOSS[name]
    except KeyError:
        raise SystemExit(f"docs/make_arch_deck.py: add a TOOL_GLOSS line for the new tool {name!r}") from None


def facts() -> dict:
    from voc.agent.tools import READ_TOOLS, TOOL_SPECS

    def lines(d: Path) -> tuple[int, int]:
        files = [p for p in d.rglob("*") if p.suffix in CODE_SUFFIXES and "__pycache__" not in str(p)]
        return len(files), sum(sum(1 for _ in p.open(encoding="utf-8", errors="replace")) for p in files)

    modules = [(m, *lines(ROOT / "voc" / m)) for m in
               ("taxonomy", "schemas", "llm", "ingest", "extract", "theme", "analytics", "store",
                "agent", "api", "web")]

    cache = {}
    cache_dir = ROOT / "data" / "cache"
    if cache_dir.exists():
        for stage in sorted(cache_dir.iterdir()):
            n = len(list(stage.rglob("*.json")))
            if n:
                cache[stage.name] = n

    meta = json.loads((ROOT / "data/meta.json").read_text(encoding="utf-8"))
    con = sqlite3.connect(ROOT / "data/voc.sqlite")
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "AND name NOT LIKE '%_fts%' ORDER BY name")]
    answers = con.execute("SELECT COUNT(*) FROM answers_cache").fetchone()[0]

    tests = len(list((ROOT / "tests").glob("test_*.py")))
    return {
        "tools": [{"name": s["name"], "desc": _gloss(s["name"]),
                   "args": list(s["input_schema"]["properties"])} for s in TOOL_SPECS],
        "n_read_tools": len(READ_TOOLS), "modules": modules, "cache": cache, "tables": tables,
        "answers": answers, "meta": meta, "test_files": tests,
        "total_lines": sum(n for _, _, n in modules),
    }


# --- extra layout helpers ----------------------------------------------------------------------

def box(slide, left, top, width, height, *, title, lines_, accent=RULE, fill=(0xFF, 0xFF, 0xFD),
        title_size=13, body_size=10.5):
    from pptx.dml.color import RGBColor

    card = slide.shapes.add_shape(1, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(*fill)
    card.line.color.rgb = accent
    card.line.width = Pt(1.0)
    card.shadow.inherit = False
    frame = card.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.14)
    frame.margin_top = Inches(0.1)
    para(frame, title, size=title_size, bold=True, color=INK, space_after=5, first=True)
    for line in lines_:
        para(frame, line, size=body_size, color=MUTED, space_after=2)
    return card


def arrow(slide, x1, y1, x2, y2, *, color=ACCENT):
    conn = slide.shapes.add_connector(2, x1, y1, x2, y2)
    conn.line.color.rgb = color
    conn.line.width = Pt(1.5)
    return conn


def lane(slide, top, height, label, *, fill=(0xF4, 0xF3, 0xEC)):
    from pptx.dml.color import RGBColor

    band = slide.shapes.add_shape(1, MARGIN, top, BODY_W, height)
    band.fill.solid()
    band.fill.fore_color.rgb = RGBColor(*fill)
    band.line.fill.background()
    band.shadow.inherit = False
    tag = textbox(slide, Emu(int(MARGIN + Inches(0.12))), Emu(int(top + Inches(0.06))), Inches(3), Inches(0.3))
    para(tag, label.upper(), size=9.5, bold=True, color=MUTED, space_after=0, first=True)
    return band


# --- slides -------------------------------------------------------------------------------------

def build(f: dict, out: Path) -> Path:
    from pptx import Presentation
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H

    # 1. Title
    s = blank(prs)
    band = s.shapes.add_shape(1, Emu(0), Emu(0), Inches(0.22), H)
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()
    band.shadow.inherit = False
    frame = textbox(s, MARGIN, Inches(2.3), Inches(10.6), Inches(3))
    para(frame, "ARCHITECTURE", size=13, bold=True, color=ACCENT, space_after=16, first=True)
    para(frame, "How the system is put together", size=40, bold=True, color=INK, space_after=18)
    para(frame, "Files are the truth. The index is derived. Every model call is cached by its content, "
                "so the whole pipeline runs offline and re-runs for free.", size=18, color=MUTED, space_after=0)
    footer(s, f"{f['total_lines']:,} lines across {len(f['modules'])} modules  ·  "
              f"{f['test_files']} test files  ·  no build step, no external services")

    # 2. The shape of it
    s = blank(prs)
    heading(s, "The shape of it", "Three layers, one direction of travel")
    lane(s, Inches(2.2), Inches(1.35), "source of truth  ·  plain files, versioned")
    gap = Inches(0.2)
    pad = Inches(0.15)
    widths = Emu(int((BODY_W - 2 * pad - 4 * gap) / 5))   # five boxes inside the lane, never off the edge
    items = [("data/calls.jsonl", ["4,425 contacts", "the corpus"]),
             ("data/extractions.jsonl", ["one reading per", "contact"]),
             ("data/themes/", ["registry, members,", "merge history"]),
             ("data/answers/", ["recorded Q&A runs"]),
             ("data/cache/", ["every model call,", "keyed by content"])]
    for i, (title, body) in enumerate(items):
        box(s, Emu(int(MARGIN + pad + i * (widths + gap))), Inches(2.55), widths, Inches(0.9),
            title=title, lines_=body, title_size=11.5, body_size=9.5)

    lane(s, Inches(3.85), Inches(1.15), "derived  ·  rebuilt in seconds")
    box(s, Emu(int(MARGIN + pad)), Inches(4.2), Emu(int(BODY_W - 2 * pad)), Inches(0.65),
        title="data/voc.sqlite", lines_=[f"{len(f['tables'])} tables, materialised trends and emerging scores "
                                         f"for every as-of week  ·  `voc build-db` recreates it from the files above"],
        title_size=11.5, body_size=9.5, accent=ACCENT)

    lane(s, Inches(5.25), Inches(1.6), "serving  ·  one process")
    for i, (title, body) in enumerate([
            ("FastAPI", ["read endpoints", "+ SSE event stream"]),
            ("Tools", [f"{f['n_read_tools']} read-only", "SQL tools"]),
            ("Agent", ["manual tool loop", "live or replayed"]),
            ("Verifier", ["recounts every", "claim server-side"]),
            ("Dashboard", ["ES modules,", "no build step"])]):
        box(s, Emu(int(MARGIN + pad + i * (widths + gap))), Inches(5.6), widths, Inches(1.0),
            title=title, lines_=body, title_size=11.5, body_size=9.5)
    footer(s, "Nothing flows upward: the index never becomes a source, and the interface never writes the corpus.")

    # 3. The pipeline
    s = blank(prs)
    heading(s, "The pipeline", "Twelve commands, every one resumable")
    rows = [
        ["voc ingest pull", "regulator API, month by month, cached on disk", "-> data/raw/"],
        ["voc ingest profile", "the support gate that sets the corpus size", "-> profile.json"],
        ["voc ingest sample", "hash-based constant fraction, fixed seed", "-> calls.jsonl"],
        ["voc extract", "one model call per contact, strict schema", "-> extractions.jsonl"],
        ["voc theme run", "seed, consolidate, rename, reassign, stability", "-> themes/"],
        ["voc build-db", "files -> SQLite, then materialise trends", "-> voc.sqlite"],
        ["voc qa", "extraction quality metrics, stored in the index", "-> meta"],
        ["voc ask / serve", "the agent and the dashboard", "-> answers/"],
    ]
    table(s, ["Command", "What it does", "Output"], rows, top=Inches(2.3),
          widths=[Inches(2.9), Inches(6.2), Inches(2.5)], highlight=(3, 4))
    frame = textbox(s, MARGIN, Inches(6.1), BODY_W, Inches(0.9))
    para(frame, "Every stage caches each model call by a content hash of its own input.", size=16, bold=True,
         color=ACCENT, space_after=6, first=True)
    para(frame, "A killed run resumes where it stopped, a re-run costs nothing, and changing the taxonomy "
                "bumps a version that is part of the key, which re-reads the corpus on purpose.",
         size=13, color=MUTED, space_after=0)

    # 4. The tools
    s = blank(prs)
    heading(s, "The tools", f"{f['n_read_tools']} read-only tools, plus one that ends the turn")
    rows = [[t["name"], t["desc"]] for t in f["tools"] if t["name"] != "submit_answer"]
    table(s, ["Tool", "What it returns"], rows, top=Inches(2.22),
          widths=[Inches(3.0), Inches(8.6)], size=11.5)
    sub = next(t for t in f["tools"] if t["name"] == "submit_answer")
    frame = textbox(s, MARGIN, Inches(6.35), BODY_W, Inches(0.8))
    para(frame, f"submit_answer  ·  {', '.join(sub['args'])}", size=13, bold=True, color=ACCENT,
         space_after=5, first=True)
    para(frame, "Terminal, and must be alone in its turn. Everything else is read-only: the agent can query "
                "the index but can never write to it.", size=12, color=MUTED, space_after=0)

    # 5. The envelope
    s = blank(prs)
    heading(s, "One envelope for every tool", "The contract that makes verification possible")
    box(s, MARGIN, Inches(2.25), Inches(5.9), Inches(3.5), title="What a tool returns", lines_=[
        "result_id     the id a claim cites",
        "tool, args    what was asked",
        "scope         how many calls are in the filtered slice",
        "summary       one line the model reads without parsing",
        "rows, data    the actual findings",
        "call_ids      up to 50 shown; n_call_ids is the true count",
        "sql           the statements, kept so they can be re-run",
        "data_version  which corpus this came from",
    ], title_size=14, body_size=11.5, accent=ACCENT)
    box(s, Emu(int(MARGIN + Inches(6.2))), Inches(2.25), Inches(5.9), Inches(3.5),
        title="Why it is shaped this way", lines_=[
        "A claim cites result_ids, not numbers.",
        "",
        "The server re-reads those results' full call-id lists,",
        "recounts them, and overrides whatever the model said.",
        "",
        "The stored SQL means a number is still explainable",
        "after the index is rebuilt: the query re-executes and",
        "the call list comes back.",
        "",
        "Results are keyed by question, because result ids",
        "restart at r1 for every question asked.",
    ], title_size=14, body_size=11.5)
    footer(s, "Tool results are persisted, so \"which calls?\" works months later, not just during the run.")

    # 6. Offline mechanics
    s = blank(prs)
    heading(s, "Running with no API key", "The offline mechanic, and why it exists")
    bullets(s, [
        ("Every LLM stage can export work bundles.", "A bundle carries the exact prompt, the records, the "
         "JSON schema and the cache identity to write. A build-time agent fills it and writes the same cache "
         "file the API path would have written."),
        ("The runner does not care who did the reading.", "A `produced_by` field records it. A fake-produced "
         "index is refused unless explicitly asked for, and then the interface shows a red warning."),
        ("Answers are recorded the same way.", "Drive the real tools from the shell, write the answer JSON, "
         "and finalize runs it through the same verifier a live answer uses."),
    ], top=Inches(2.25), size=16)
    biggest = sorted(f["cache"].items(), key=lambda kv: -kv[1])[:4]
    stats = [(f"{n:,}", stage.replace("_", " ")) for stage, n in biggest]
    stats.append((str(f["answers"]), "recorded answers"))
    stat_row(s, stats, top=Inches(5.15), height=Inches(1.3))
    footer(s, f"This is how all {f['meta']['n_calls']:,} contacts were read and all "
              f"{f['meta']['n_members']:,} statements grouped, on a machine with no key.")

    # 7. Three modes
    s = blank(prs)
    heading(s, "Three ways to answer", "Same tools, same verifier, different source of judgement")
    cols = [
        ("LIVE", "an agent calls the model", [
            "The agent picks tools itself.",
            "Streams its reasoning and every call.",
            "Round and time budgets bound it.",
            "Needs a key. Costs per question.",
        ], ACCENT),
        ("RECORDED", "a real run, replayed", [
            "A past live run, re-verified on the way out.",
            "Matched exactly, or by token overlap.",
            "About two seconds, no key, no network.",
            "This is what the demo uses.",
        ], POSITIVE),
        ("TEMPLATED", "no model at all", [
            "Eight regex archetypes route the question.",
            "Pulls from the same tools.",
            "Numbers are real; the prose is a template.",
            "Always badged on screen.",
        ], RGBColor(0x6B, 0x72, 0x80)),
    ]
    width = Inches(3.85)
    for i, (name, sub, lines_, colour) in enumerate(cols):
        left = Emu(int(MARGIN + i * (width + Inches(0.28))))
        bar = s.shapes.add_shape(1, left, Inches(2.3), width, Inches(0.07))
        bar.fill.solid()
        bar.fill.fore_color.rgb = colour
        bar.line.fill.background()
        bar.shadow.inherit = False
        frame = textbox(s, Emu(int(left + Inches(0.02))), Inches(2.52), width, Inches(0.8))
        para(frame, name, size=19, bold=True, color=INK, space_after=2, first=True)
        para(frame, sub, size=12, italic=True, color=colour, space_after=0)
        body = textbox(s, Emu(int(left + Inches(0.02))), Inches(3.45), width, Inches(2.4))
        for j, line in enumerate(lines_):
            para(body, line, size=12.5, color=MUTED, space_after=9, first=(j == 0))
    frame = textbox(s, MARGIN, Inches(6.1), BODY_W, Inches(0.9))
    para(frame, "All three go through the same server-side verification before anything is rendered.",
         size=16, bold=True, color=ACCENT, space_after=5, first=True)
    para(frame, "That is what makes the fallbacks honest rather than embarrassing: a templated answer's "
                "numbers are as checked as a live one's.", size=13, color=MUTED, space_after=0)

    # 8. Provider abstraction
    s = blank(prs)
    heading(s, "Not tied to one model", "The provider is an adapter, not a fork")
    bullets(s, [
        ("Batch stages speak one interface.", "`complete_json(LLMRequest) -> LLMResult`, with three "
         "implementations behind it: the live API, the cache, and a deterministic fake for tests."),
        ("The agent loop takes an injectable turn.", "It hands over messages and reads content blocks back. "
         "Swapping provider means writing one adapter that translates in both directions, not rewriting "
         "the loop, the budgets, the tool execution or the verifier."),
        ("Verified in practice, not in principle.", "A live run on Gemini through OpenRouter: six claims, "
         "every one recounted and verified, no number mismatches, no dropped quotes."),
    ], top=Inches(2.25), size=16)
    frame = textbox(s, MARGIN, Inches(5.1), BODY_W, Inches(1.5))
    para(frame, "A different model can choose different tools. It cannot make a number wrong.",
         size=19, bold=True, color=ACCENT, space_after=8, first=True)
    para(frame, "The server recounts every claim from call ids and checks every quoted figure against the "
                "tool result it cites, whichever model proposed them. Where the evidence retrieved is "
                "thinner, the confidence badge says so by itself.", size=14, color=MUTED, space_after=0)

    # 9. Verification path
    s = blank(prs)
    heading(s, "The verification path", "What happens between the model and the screen")
    steps = [
        ("1", "Claim cites result_ids", "never raw numbers"),
        ("2", "Server re-reads those results", "full call-id lists, scoped to this question"),
        ("3", "Recount", "the server's number wins over the model's"),
        ("4", "Check every figure", "must appear in a cited tool result"),
        ("5", "Check every quote", "must be an exact substring of the source text"),
        ("6", "Compute confidence", "from calls, months, products and states"),
    ]
    top = Inches(2.3)
    for num, title, sub in steps:
        chip = s.shapes.add_shape(1, MARGIN, top, Inches(0.42), Inches(0.42))
        chip.fill.solid()
        chip.fill.fore_color.rgb = ACCENT
        chip.line.fill.background()
        chip.shadow.inherit = False
        cf = chip.text_frame
        cf.margin_left = cf.margin_right = cf.margin_top = cf.margin_bottom = 0
        from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
        cf.vertical_anchor = MSO_ANCHOR.MIDDLE
        para(cf, num, size=14, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), align=PP_ALIGN.CENTER,
             space_after=0, first=True)
        frame = textbox(s, Emu(int(MARGIN + Inches(0.62))), Emu(int(top + Inches(0.02))), Inches(10.8), Inches(0.5))
        p = para(frame, title, size=15, bold=True, color=INK, space_after=0, first=True)
        run = p.add_run()
        run.text = "   " + sub
        run.font.size = Pt(13)
        run.font.color.rgb = MUTED
        run.font.name = "Segoe UI"
        top = Emu(int(top + Inches(0.62)))
    frame = textbox(s, MARGIN, Inches(6.3), BODY_W, Inches(0.8))
    para(frame, "A claim that survives none of this is shown greyed, with the server's real number beside it. "
                "It is never quietly deleted.", size=14, bold=True, color=POSITIVE, space_after=0, first=True)

    # 10. Modules
    s = blank(prs)
    heading(s, "The code", "Where each thing lives")
    blurbs = {
        "taxonomy": "the enums, their definitions, and the regulator mapping used for QA",
        "schemas": "call, extraction, theme, filter and answer contracts (pydantic + strict JSON schema)",
        "llm": "one interface over live, cached and fake clients, plus the cost table",
        "ingest": "API pull, the support gate, hash sampling, transcript normaliser",
        "extract": "step 1: prompt, async runner, quote verification, work bundles",
        "theme": "step 2: bucketing, four passes, the merge audit trail, stability",
        "analytics": "step 3: Wilson intervals, the emerging score, segment lift, confidence tiers",
        "store": "the SQLite schema, the builder, and every query the tools run",
        "agent": "steps 4 and 5: tools, the loop, the verifier, the cache, the offline analyst",
        "api": "FastAPI endpoints and the event stream",
        "web": "the dashboard: static ES modules, vendored chart library, no build step",
    }
    rows = [[f"voc/{m}/", blurbs[m], f"{n:,}"] for m, _, n in f["modules"]]
    table(s, ["Module", "What it holds", "Lines"], rows, top=Inches(2.25),
          widths=[Inches(1.9), Inches(8.3), Inches(1.4)], size=11.5, highlight=(7, 8))
    footer(s, f"{f['total_lines']:,} lines in all. The two highlighted modules are where the interesting "
              f"decisions live: what the data means, and what may be shown.")

    # 11. Operational properties
    s = blank(prs)
    heading(s, "Properties worth knowing", "The things that shape every change you make")
    bullets(s, [
        ("The counting unit is the contact.", "A theme, reason or driver counts at most once per contact, "
         "and every share is over the contacts in the same filtered slice."),
        ("Minimum support is deliberate.", "Nothing is ranked below five contacts; a segment cell is blanked "
         "below fifty in the slice. Relaxing it to make a chart look fuller is the wrong fix."),
        ("Quotes must be exact substrings.", "An exact or whitespace-normalised match, nothing else. "
         "Unverified quotes never reach the interface, a tool result, or the agent."),
        ("The as-of week must be complete.", "A corpus ending mid-week puts a half-empty week in the recent "
         "window and hides every emerging signal."),
        ("The index is disposable.", "Rebuilt from files in about four seconds, including restoring the "
         "recorded answers and the tool results behind their numbers."),
    ], top=Inches(2.25), size=15.5)

    # 12. Close
    s = blank(prs)
    band = s.shapes.add_shape(1, Emu(0), Emu(0), Inches(0.22), H)
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()
    band.shadow.inherit = False
    frame = textbox(s, MARGIN, Inches(1.7), Inches(11.0), Inches(1))
    para(frame, "WHY IT IS BUILT THIS WAY", size=13, bold=True, color=ACCENT, space_after=20, first=True)
    top = Inches(2.75)
    for label, rest in [
        ("Because the demo has to run anywhere.", "No external services, no key required, no network. "
         "Clone, build the index, serve."),
        ("Because re-running has to be free.", "Content-hash caching means tomorrow's contacts cost only "
         "tomorrow's contacts, and a killed run resumes."),
        ("Because a bank will ask where the number came from.", "Every figure traces to a query, and the "
         "query re-executes to a list of real calls you can open and read."),
    ]:
        fr = textbox(s, MARGIN, top, Inches(11.4), Inches(1.05))
        para(fr, label, size=22, bold=True, color=INK, space_after=4, first=True)
        para(fr, rest, size=14, color=MUTED, space_after=0)
        top = Emu(int(top + Inches(1.25)))

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "voc_architecture_deck.pptx"
    path = build(facts(), target)
    print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
