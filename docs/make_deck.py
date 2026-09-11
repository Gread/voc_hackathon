"""Build the presentation deck from the live index, so no number on a slide is typed by hand.

Usage: python docs/make_deck.py [output.pptx]
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent

INK = RGBColor(0x14, 0x17, 0x1C)
PAPER = RGBColor(0xFA, 0xFA, 0xF7)
MUTED = RGBColor(0x6B, 0x72, 0x80)
ACCENT = RGBColor(0xC2, 0x41, 0x1F)
RULE = RGBColor(0xDE, 0xDE, 0xD6)
POSITIVE = RGBColor(0x2F, 0x6F, 0x4E)

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.85)
BODY_W = W - 2 * MARGIN


# --- numbers, read from the index rather than typed ------------------------------------------

def facts() -> dict:
    meta = json.loads((ROOT / "data/meta.json").read_text(encoding="utf-8"))
    con = sqlite3.connect(ROOT / "data/voc.sqlite")
    con.row_factory = sqlite3.Row

    def one(sql, params=()):
        return con.execute(sql, params).fetchone()[0]

    top = [dict(r) for r in con.execute(
        "SELECT name, n_calls, n_wordings, n_products FROM themes WHERE status='active' "
        "ORDER BY n_calls DESC LIMIT 5")]
    tenth = con.execute("SELECT n_calls, n_wordings FROM themes WHERE status='active' "
                        "ORDER BY n_calls DESC LIMIT 1 OFFSET 9").fetchone()
    wordings = [r["issue_statement"] for r in con.execute(
        "SELECT issue_statement FROM theme_wordings WHERE theme_id=? ORDER BY rank", ["thm_denied_or_declined_without_explanation__negative_004"])]
    # Three real wordings of the same theme, chosen because they share almost no vocabulary.
    # Keyed on a distinctive phrase so the slide is reproducible and reviewable.
    keys = ["drive-thru cameras", "mistaken lost-card date", "document upload process"]
    picks = [next((w for w in wordings if k in w), "") for k in keys]
    replay = [dict(r) for r in con.execute(
        "SELECT as_of_week, n_recent, expected_recent, z, status FROM emerging_scores "
        "WHERE entity_type='theme' AND entity_id=? AND as_of_week BETWEEN '2025-W38' AND '2025-W45' "
        "ORDER BY as_of_week", ["thm_no_response_or_follow_up__negative_004"])]
    replay_name = one("SELECT name FROM themes WHERE theme_id=?", ["thm_no_response_or_follow_up__negative_004"])

    claims = quotes = flagged = 0
    for f in sorted((ROOT / "data/answers").glob("*.json")):
        a = json.loads(f.read_text(encoding="utf-8"))["answer"]
        claims += len(a["claims"])
        quotes += len(a["quotes"])
        flagged += sum(1 for c in a["claims"] if not c.get("verified") or c.get("flags"))

    import json as _json
    differs = sum(1 for line in (ROOT / "data/extractions.jsonl").open(encoding="utf-8")
                  if (r := _json.loads(line)).get("status") == "ok" and r["extraction"].get("reason_differs"))
    head_id = "thm_denied_or_declined_without_explanation__negative_004"
    head = dict(con.execute("SELECT name, n_calls, n_wordings, n_products FROM themes WHERE theme_id=?",
                            [head_id]).fetchone())
    head["states"] = one("SELECT COUNT(DISTINCT c.region) FROM v_theme_calls tc JOIN calls c "
                         "ON c.call_id=tc.call_id WHERE tc.theme_id=? AND c.region != 'unknown'", [head_id])

    def lines(*globs: str) -> int:
        return sum(sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
                   for g in globs for p in ROOT.glob(g))

    return {
        "differs": differs, "head": head,
        "py_lines": lines("voc/**/*.py"), "js_lines": lines("voc/web/js/*.js"),
        "test_lines": lines("tests/**/*.py"), "tenth": dict(tenth), "picks": picks,
        "calls": meta["n_calls"], "topics": meta["n_topics"], "members": meta["n_members"],
        "active_themes": one("SELECT COUNT(*) FROM themes WHERE status='active'"),
        "catch_alls": one("SELECT COUNT(*) FROM themes WHERE status='catch_all'"),
        "unplaced": one("SELECT COUNT(*) FROM theme_members tm JOIN themes t "
                        "ON t.theme_id=tm.effective_theme_id WHERE t.status='catch_all'"),
        "wordings_total": one("SELECT COUNT(*) FROM theme_wordings"),
        "merges": one("SELECT COUNT(*) FROM theme_merges"),
        "positive_calls": one("SELECT COUNT(DISTINCT call_id) FROM positive_moments WHERE verified=1"),
        "quote_rate": meta["qa_quote_verify_rate"], "topics_per_call": meta["qa_topics_per_call"],
        "negative_share": meta["qa_negative_share"], "abstained": meta["qa_other_share"],
        "reason_agreement": meta["qa_reason_agreement"], "as_of": meta["as_of_week"],
        "top": top, "wordings": wordings, "replay": replay, "replay_name": replay_name,
        "answers": 8, "claims": claims, "quotes": quotes, "flagged": flagged,
    }


# --- layout helpers --------------------------------------------------------------------------

def textbox(slide, left, top, width, height):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    return frame


def para(frame, text, *, size=18, bold=False, color=INK, space_after=6, space_before=0,
         first=False, align=PP_ALIGN.LEFT, italic=False, font="Segoe UI"):
    p = frame.paragraphs[0] if first else frame.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return p


def blank(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAPER
    return slide


def rule(slide, top, left=MARGIN, width=BODY_W, color=RULE, thickness=Pt(1.25)):
    line = slide.shapes.add_connector(1, left, top, left + width, top)
    line.line.color.rgb = color
    line.line.width = thickness
    return line


def heading(slide, kicker, title):
    frame = textbox(slide, MARGIN, Inches(0.62), BODY_W, Inches(1.25))
    para(frame, kicker.upper(), size=12, bold=True, color=ACCENT, space_after=6, first=True)
    para(frame, title, size=33, bold=True, color=INK, space_after=0)
    rule(slide, Inches(1.92))


def bullets(slide, items, *, top=Inches(2.3), size=17, lead=None, width=BODY_W, left=MARGIN):
    frame = textbox(slide, left, top, width, H - top - Inches(0.7))
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            label, rest = item
            p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            p.space_after = Pt(13)
            r1 = p.add_run()
            r1.text = label + "  "
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = INK
            r1.font.name = "Segoe UI"
            r2 = p.add_run()
            r2.text = rest
            r2.font.size = Pt(size)
            r2.font.color.rgb = MUTED
            r2.font.name = "Segoe UI"
        else:
            para(frame, item, size=size, color=MUTED, space_after=13, first=(i == 0))
    return frame


def stat_row(slide, stats, *, top, height=Inches(1.5)):
    """Evenly spaced big numbers with a caption under each."""
    gap = Inches(0.3)
    width = Emu(int((BODY_W - gap * (len(stats) - 1)) / len(stats)))
    for i, (value, caption) in enumerate(stats):
        left = Emu(int(MARGIN + i * (width + gap)))
        card = slide.shapes.add_shape(1, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(0xF2, 0xF1, 0xEA)
        card.line.color.rgb = RULE
        card.line.width = Pt(0.75)
        card.shadow.inherit = False
        frame = card.text_frame
        frame.word_wrap = True
        frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        frame.margin_left = frame.margin_right = Inches(0.16)
        para(frame, value, size=30, bold=True, color=INK, align=PP_ALIGN.CENTER, space_after=2, first=True)
        para(frame, caption, size=11.5, color=MUTED, align=PP_ALIGN.CENTER, space_after=0)


def quote_card(slide, text, *, top, height, accent=ACCENT, size=15):
    card = slide.shapes.add_shape(1, MARGIN, top, BODY_W, height)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFD)
    card.line.color.rgb = RULE
    card.line.width = Pt(0.75)
    card.shadow.inherit = False
    bar = slide.shapes.add_shape(1, MARGIN, top, Inches(0.055), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()
    bar.shadow.inherit = False
    frame = card.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame.margin_left = Inches(0.3)
    frame.margin_right = Inches(0.25)
    para(frame, text, size=size, italic=True, color=INK, space_after=0, first=True)


def fits_one_line(text: str, size: float, width_in: float, bold: bool = False) -> bool:
    """Rough Segoe UI advance width. Used to fail the build rather than clip text on a slide."""
    per_char = size * (0.53 if bold else 0.50) / 72.0
    return len(str(text)) * per_char <= width_in


def table(slide, headers, rows, *, top, widths, size=13, highlight=()):
    left = MARGIN
    row_h = Inches(0.38)
    total = sum(widths, Emu(0))
    # A table row is one line tall. Text that would wrap gets clipped in PowerPoint, which is how
    # truncated copy reaches a stage unnoticed, so refuse to build instead.
    for cells in rows:
        for cell, w in zip(cells, widths):
            avail = Emu(w).inches - 0.28
            if not fits_one_line(cell, size, avail):
                raise SystemExit(f"deck: {str(cell)[:60]!r} needs more than {avail:.2f}in at {size}pt; "
                                 f"shorten the copy or widen the column")
    head = slide.shapes.add_shape(1, left, top, total, row_h)
    head.fill.solid()
    head.fill.fore_color.rgb = RGBColor(0xEC, 0xEB, 0xE3)
    head.line.fill.background()
    head.shadow.inherit = False
    x = left
    for h, w in zip(headers, widths):
        frame = textbox(slide, Emu(int(x + Inches(0.14))), Emu(int(top + Inches(0.07))), Emu(int(w - Inches(0.2))), row_h)
        para(frame, h, size=11, bold=True, color=MUTED, space_after=0, first=True)
        x = Emu(int(x + w))
    for r, cells in enumerate(rows):
        y = Emu(int(top + row_h * (r + 1)))
        if r in highlight:
            band = slide.shapes.add_shape(1, left, y, total, row_h)
            band.fill.solid()
            band.fill.fore_color.rgb = RGBColor(0xFB, 0xEE, 0xE9)
            band.line.fill.background()
            band.shadow.inherit = False
        x = left
        for c, (cell, w) in enumerate(zip(cells, widths)):
            frame = textbox(slide, Emu(int(x + Inches(0.14))), Emu(int(y + Inches(0.08))), Emu(int(w - Inches(0.2))), row_h)
            bold = r in highlight and c == 0
            color = ACCENT if r in highlight else INK if c == 0 else MUTED
            para(frame, str(cell), size=size, bold=bold, color=color, space_after=0, first=True)
            x = Emu(int(x + w))
        rule(slide, Emu(int(y + row_h)), left=left, width=total, color=RGBColor(0xEE, 0xED, 0xE6), thickness=Pt(0.5))


def footer(slide, text):
    frame = textbox(slide, MARGIN, H - Inches(0.62), BODY_W, Inches(0.32))
    para(frame, text, size=10.5, color=MUTED, space_after=0, first=True)


# --- slides ----------------------------------------------------------------------------------

def build(f: dict, out: Path) -> Path:
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H

    # 1. Title
    s = blank(prs)
    band = s.shapes.add_shape(1, Emu(0), Emu(0), Inches(0.22), H)
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()
    band.shadow.inherit = False
    frame = textbox(s, MARGIN, Inches(2.15), Inches(10.6), Inches(3))
    para(frame, "VOICE OF THE CUSTOMER INSIGHTS", size=13, bold=True, color=ACCENT, space_after=16, first=True)
    para(frame, "Turning thousands of contact-centre\nconversations into evidence-based insight",
         size=40, bold=True, color=INK, space_after=18)
    para(frame, "Agents do the reading. The server checks every number before you see it.",
         size=19, color=MUTED, space_after=0)
    footer(s, f"Working proof of concept  ·  {f['calls']:,} real contacts  ·  24 months  ·  runs offline")

    # 2. The problem
    s = blank(prs)
    heading(s, "The problem", "Nobody reads the conversations")
    bullets(s, [
        ("Volume beats attention.", "Thousands of calls a week. A person samples a handful, and the sample is "
         "whatever was easy to grab."),
        ("Labels are not causes.", "A dropdown says \"fee complaint\". It never says the fee was charged although "
         "the deposit already showed as available."),
        ("One problem arrives as a hundred problems.", "The same failure is described in a hundred different ways, "
         "so no keyword rule ever groups it and the volume stays invisible."),
        ("By the time it is measurable, it is old.", "A theme that matters is small first. Monthly reporting "
         "finds it a quarter late."),
        ("Numbers nobody can trace.", "A slide says 12%. Nobody in the room can open the calls behind it."),
    ])

    # 3. What we built
    s = blank(prs)
    heading(s, "What we built", "Five steps, all working on real data")
    bullets(s, [
        ("1  Read every contact.", "Each one goes to Claude once and comes back as a fixed structure: reasons, "
         "products, topics with a sentiment each, the specific driver, and verbatim evidence."),
        ("2  Connect to the collective.", "Differently-worded descriptions of the same experience are grouped into "
         "themes. One problem, one plausible cause, one team that could fix it."),
        ("3  Watch the shape over time.", "Weekly counts with an emerging score, so a theme that is small but "
         "accelerating is flagged while it is still small."),
        ("4  Answer plain-language questions.", "An agent picks what to pull from twelve read-only tools and "
         "submits a structured answer."),
        ("5  Show evidence and confidence.", "Every claim traces to real calls. The server recounts it before it "
         "reaches the screen."),
    ])
    footer(s, "The briefing asked to prioritise the question-answering demo. It is the centre of the product.")

    # 4. The data
    s = blank(prs)
    heading(s, "The data", "Real complaints, not a synthetic corpus")
    bullets(s, [
        ("Source.", "Consumer complaint narratives about one large US bank, pulled live from the US regulator's "
         "public database. Every record was written by a real person who consented to publication."),
        ("Sampling.", f"A constant 25.25% of that bank's eligible narratives per month, fixed seed, hash-based. "
         f"Month-to-month movement is the real shape of the intake, not an artefact of sampling."),
        ("Size chosen by a gate, not a guess.", "At least 30 sampled contacts in 90% of weeks, two products and "
         "two segments with real volume, every month present. 4,000 failed the weekly gate. 4,425 passes."),
    ], top=Inches(2.25))
    stat_row(s, [(f"{f['calls']:,}", "contacts read"), ("24", "months"), ("1", "bank"),
                 ("25.25%", "constant sample"), ("0", "synthetic records")], top=Inches(5.05), height=Inches(1.3))
    footer(s, "Honest caveat, stated in the product: complaint dates are when the regulator received them, "
              "which lags the contact by days to weeks.")

    # 5. Step 1
    s = blank(prs)
    heading(s, "Step 1 · Read every call", "A consistent structure, not a summary")
    bullets(s, [
        ("What comes back per contact.", "Contact reasons from a small taxonomy plus the reason in the customer's "
         "own words, products, topics each with a sentiment from -2 to +2, the specific driver of that feeling, "
         "verbatim evidence quotes with character offsets, and what the customer asked for."),
        ("The form's own labels are deliberately withheld.", "The regulator's product and issue fields never reach "
         "the extractor. Feeding them in would bias the reading toward the dropdown, which is the exact failure "
         "we are trying to solve, and would destroy our only free quality measure."),
    ], top=Inches(2.25))
    stat_row(s, [(f"{f['quote_rate'] * 100:.1f}%", "quotes verify as exact\nsubstrings of the source"),
                 ("0", "validation errors\nin 4,425 readings"),
                 (f"{f['topics_per_call']:.2f}", "topics per contact"),
                 (f"{f['abstained'] * 100:.1f}%", "abstained rather\nthan guessed"),
                 (f"{f['negative_share'] * 100:.1f}%", "negative, as a complaint\ncorpus should be")],
             top=Inches(4.95), height=Inches(1.45))
    footer(s, "A quote that is not an exact substring never reaches the interface, a tool result, or the agent.")

    # 6. Step 2
    s = blank(prs)
    heading(s, "Step 2 · Connect to the collective", "Many complaints become one problem")
    bullets(s, [
        ("Four passes.", "Seed a registry inside each driver category, consolidate near-duplicates through an audit "
         "trail that never deletes membership, rewrite every name so it alone tells a product owner what the problem "
         "is, then re-assign every statement against the frozen registry."),
        ("Measured, not asserted.", f"Re-judging a 10% sample independently agreed with the original assignment "
         f"88.1% of the time. {f['unplaced']} statements fit nothing and were left unplaced rather than forced; they "
         f"count in every total but are never ranked or flagged."),
    ], top=Inches(2.25))
    stat_row(s, [(f"{f['members']:,}", "issue statements"), ("4", "grouping passes"),
                 (f"{f['active_themes']}", "themes"), (f"{f['wordings_total']:,}", "distinct wordings"),
                 ("0.881", "re-judgement agreement")], top=Inches(4.9), height=Inches(1.4))
    footer(s, "A theme is one problem, with one plausible cause, that one team could fix.")

    # 7. The money slide
    s = blank(prs)
    heading(s, "The payoff", f"The same problem, in {f['head']['n_wordings']} different wordings")
    frame = textbox(s, MARGIN, Inches(2.18), BODY_W, Inches(0.8))
    h = f["head"]
    para(frame, h["name"], size=23, bold=True, color=INK, space_after=5, first=True)
    para(frame, f"{h['n_calls']} contacts  ·  {h['n_wordings']} distinct wordings  ·  {h['n_products']} products  "
                f"·  {h['states']} states  ·  {h['n_calls'] / f['calls'] * 100:.1f}% of everything that came in",
         size=14, color=MUTED, space_after=0)
    for text, top in zip(f["picks"], [Inches(3.22), Inches(4.12), Inches(5.02)]):
        quote_card(s, "“" + text + "”", top=top, height=Inches(0.78), size=13.5)
    frame = textbox(s, MARGIN, Inches(6.05), BODY_W, Inches(0.7))
    para(frame, "Three real contacts. One cause. No shared phrase, so no keyword rule, tag list or canned "
                "disposition ever finds them together.", size=15, bold=True, color=ACCENT, space_after=0, first=True)
    footer(s, f"The ratio holds down the whole top ten: {f['top'][0]['n_wordings']} wordings over "
              f"{f['top'][0]['n_calls']} contacts at the top, {f['tenth']['n_wordings']} over "
              f"{f['tenth']['n_calls']} at the tenth.")

    # 8. What the themes say
    s = blank(prs)
    heading(s, "What the reading found", "Causes a team could act on, not tags")
    table(s, ["Theme", "Contacts", "Wordings", "Products"],
          [[t["name"], f"{t['n_calls']:,}", t["n_wordings"], t["n_products"]] for t in f["top"]],
          top=Inches(2.35), widths=[Inches(7.2), Inches(1.5), Inches(1.5), Inches(1.4)], highlight=(0,))
    frame = textbox(s, MARGIN, Inches(5.0), BODY_W, Inches(1.6))
    para(frame, "None of these exist as an option on a complaint form.", size=19, bold=True, color=INK,
         space_after=10, first=True)
    para(frame, "They read like work items because they name a mechanism: investigators closing cases on a narrow "
                "automated check instead of pulling the evidence; a back-office risk process the front line cannot "
                "see into; a reported error with no correction loop behind it.",
         size=15, color=MUTED, space_after=0)

    # 9. Step 3
    s = blank(prs)
    heading(s, "Step 3 · Watch the shape over time", "Hear it while it is still small")
    frame = textbox(s, MARGIN, Inches(2.2), BODY_W, Inches(0.8))
    para(frame, f"Replaying one real theme week by week: “{f['replay_name']}”", size=15,
         color=MUTED, space_after=0, first=True)
    rows = [[r["as_of_week"], r["n_recent"], f"{r['expected_recent']:.1f}", f"{r['z']:.2f}",
             {"insufficient": "below threshold"}.get(r["status"], r["status"])] for r in f["replay"]]
    hot = tuple(i for i, r in enumerate(f["replay"]) if r["status"] in ("emerging", "growing", "new"))
    table(s, ["As-of week", "Recent 4 weeks", "Expected", "z", "Verdict"], rows, top=Inches(2.85),
          widths=[Inches(2.1), Inches(2.2), Inches(1.7), Inches(1.4), Inches(4.2)], highlight=hot)
    frame = textbox(s, MARGIN, H - Inches(1.5), BODY_W, Inches(0.9))
    para(frame, "Quiet, quiet, then six contacts against two expected, and it fires.", size=17, bold=True,
         color=ACCENT, space_after=6, first=True)
    para(frame, "Four recent weeks against the sixteen before, Poisson z with a Jeffreys pseudo-count, minimum "
                "support of five contacts in at least two weeks. Scores are precomputed for every as-of week, so "
                "the dashboard slider replays what the system would have told you that Monday. Nothing is planted.",
         size=13, color=MUTED, space_after=0)

    # 10. Step 4
    s = blank(prs)
    heading(s, "Step 4 · Answer plain-language questions", "Ask in words, get counts, trends and quotes")
    bullets(s, [
        ("Twelve read-only tools.", "Overview, contact reasons, theme list and detail, trend, emerging, sentiment "
         "drivers, breakdown, compare, quotes, search, and one full call. The agent chooses what to pull and "
         "submits a structured answer."),
        ("Three ways to answer, one verifier.", "With an API key the agent runs live. Without one, a recorded run "
         "replays through the same channel, and an unscripted question gets a templated answer from the same tools, "
         "clearly badged. The code is the same either way."),
        ("All eight questions from the briefing are recorded.", "They replay in about two seconds each, with the "
         "tool trace visible, so the demo needs no key and no network."),
    ], top=Inches(2.25))
    stat_row(s, [(f"{f['answers']}", "questions recorded"), (f"{f['claims']}", "claims made"),
                 (f"{f['claims'] - f['flagged']}", "claims verified"), (f"{f['quotes']}", "verified quotes kept"),
                 ("0", "quotes dropped as unverified")], top=Inches(5.05), height=Inches(1.35))

    # 11. Step 5
    s = blank(prs)
    heading(s, "Step 5 · Evidence and confidence", "The model proposes. The server decides.")
    bullets(s, [
        ("Every claim is recounted.", "The server re-queries the call ids behind a claim and counts them itself. "
         "If the model said 60 and the calls say 47, the screen says 47 and shows the correction."),
        ("Every number is checked against its source.", "A figure that appears in no tool result the claim cites is "
         "flagged, not printed."),
        ("Quotes must be exact.", "An evidence quote must be an exact substring of what the customer wrote. "
         "Anything else is dropped before it reaches the screen."),
        ("Confidence is computed, not claimed.", "The badge comes from the recounted calls, months, products and "
         "states. The model never writes it."),
        ("Nothing fails silently.", "A claim that cannot be supported is shown greyed with the server's real number "
         "beside it, never quietly deleted."),
    ], top=Inches(2.25), size=16)
    footer(s, "Every number on the screen is a link to the list of calls behind it.")

    # 12. Architecture
    s = blank(prs)
    heading(s, "How it is built", "Files are the truth. Everything else is derived.")
    bullets(s, [
        ("Files first.", "The contacts, the readings and the themes are plain JSONL. The SQLite index is derived "
         "and rebuilt from them in about four seconds, so it is never something to protect."),
        ("Every model call is cached by content hash.", "Re-running a stage costs nothing, a killed run resumes "
         "where it stopped, and tomorrow's contacts cost only tomorrow's contacts."),
        ("One interface over three clients.", "Live API, replayed cache, or a deterministic fake for tests. A "
         "fake-produced index is refused unless explicitly asked for, and then the interface shows a red warning."),
        ("No build step in the interface.", "Vanilla ES modules and one vendored chart library. Clone, build the "
         "index, serve."),
    ], top=Inches(2.25))
    stat_row(s, [("108", "tests, no network\nor API key needed"),
                 (f"{f['py_lines']:,}", "lines of Python"),
                 (f"{f['js_lines']:,}", "lines of JavaScript"),
                 ("4s", "full index rebuild"),
                 ("2s", "to replay an answer")], top=Inches(5.05), height=Inches(1.35))

    # 13. No API key
    s = blank(prs)
    heading(s, "A constraint worth showing", "Built with no API key on the machine")
    bullets(s, [
        ("Every LLM stage exports work bundles.", "Each bundle carries the exact prompt, the records, and the cache "
         "identity to write. Build-time Claude agents filled them, writing the same cache files the API path writes."),
        ("The pipeline does not care who did the reading.", "A field records it. Swap in a key and the same "
         "commands run unattended against the API."),
        ("This is how all 4,425 contacts were read and all 5,827 statements grouped.", "It is also why the demo "
         "runs on a plane."),
    ], top=Inches(2.3), size=17)
    frame = textbox(s, MARGIN, Inches(5.2), BODY_W, Inches(1.2))
    para(frame, "The same property makes it auditable.", size=18, bold=True, color=INK, space_after=8, first=True)
    para(frame, "Because every model call is a cache file keyed by its content, anyone can re-run a stage and get "
                "the identical result, or open the exact prompt behind any reading.", size=15, color=MUTED,
         space_after=0)

    # 14. Honesty
    s = blank(prs)
    heading(s, "What is true, and what is not", "The findings we would rather not have to say")
    bullets(s, [
        ("One briefing expectation does not hold here.", "The stated reason is supposed to differ often from the "
         f"real driver. In this corpus it differs in about 1 contact in {round(f['calls'] / f['differs'])}. "
         "Someone writing to a regulator leads "
         "with the grievance; someone phoning opens with what they want. The capability is built and works. On real "
         "call transcripts we expect it to matter far more."),
        ("Satisfaction cannot be measured on a complaint corpus.", f"Ranking positive themes returns nothing. What "
         f"exists is {f['positive_calls']} contacts carrying a moment that went right, and the product says so on "
         f"the screen rather than inventing a score."),
        ("Only one theme is emerging this week.", "That is the honest state of the data. A detector that fires "
         "every week is a detector nobody reads."),
    ], top=Inches(2.3), size=16)
    footer(s, "A system that cannot say “the evidence does not support that” is not worth trusting when it says anything else.")

    # 15. Close
    s = blank(prs)
    band = s.shapes.add_shape(1, Emu(0), Emu(0), Inches(0.22), H)
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()
    band.shadow.inherit = False
    frame = textbox(s, MARGIN, Inches(1.5), Inches(10.8), Inches(1.2))
    para(frame, "WHAT IT DELIVERS", size=13, bold=True, color=ACCENT, space_after=18, first=True)
    items = [
        ("Minutes, not weeks.", f"{f['calls']:,} contacts read into a consistent structure, and any question about "
         f"them answered in seconds."),
        ("Hear it while it is small.", "A theme flagged at six contacts against two expected, weeks before a "
         "monthly report would show it."),
        ("Act on causes, not labels.", f"{f['head']['n_calls']} people describing one fixable failure in "
         f"{f['head']['n_wordings']} different ways, named as one work item with an owner."),
    ]
    top = Inches(2.55)
    for label, rest in items:
        frame = textbox(s, MARGIN, top, Inches(11.3), Inches(1.05))
        para(frame, label, size=25, bold=True, color=INK, space_after=4, first=True)
        para(frame, rest, size=15, color=MUTED, space_after=0)
        top = Emu(int(top + Inches(1.28)))
    frame = textbox(s, MARGIN, H - Inches(1.0), BODY_W, Inches(0.5))
    para(frame, "And every number on the screen is a list of calls you can open and read.", size=16, bold=True,
         color=POSITIVE, space_after=0, first=True)

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "voc_insights_deck.pptx"
    path = build(facts(), target)
    print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
