#!/usr/bin/env python3
"""render_commentary_prototype.py — Tiny stand-off commentary renderer.

A proof-of-concept renderer for the May 2026 commentary prototype.
Reads the canonical Apannaka-jataka passages and the four sibling
commentary files (editorial / scholarship / traditional bridge / AI)
and emits a single self-contained HTML page that demonstrates:

  - the bare-canon guarantee (commentary toggleable off)
  - the seven-layer separation (each layer rendered in its own style)
  - non-destructive overlays (the primary passage is never mutated)
  - the AI quarantine (off by default, distinct visual mark)
  - the unresolved-bridge case (Layer-3 with body=null shown as a gap)

The script is read-only with respect to the canonical library. It
writes one output file:

    06_workspace/commentary_prototype.html

This is the prototype's only deliverable artifact. Open it in a
browser to read the rendered Apannaka with the prototype commentary
layered on. Use the toggles to test the constitutional behavior.

Constitutional commitments tested by this renderer:

  - the primary text is never modified by the renderer
  - layers do not collapse: each carries its own visual register
  - anchor resolution is deterministic and explicit
  - bare-canon mode produces the canonical text verbatim
  - AI overlays start collapsed and carry their model identity

Usage:
    python 05_scripts/render_commentary_prototype.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "01_library" / "library" / "texts" / "sacred" / "buddhist" / "jataka-chalmers-vol1"
OUT_PATH = ROOT / "06_workspace" / "commentary_prototype.html"

TARGET_TALE = 1   # Apannaka

LAYER_FILES = [
    ("editorial",    "commentary_editorial.json"),
    ("scholarship",  "commentary_scholarship.json"),
    ("traditional",  "attachments_traditional.json"),
    ("ai",           "commentary_ai.json"),
]

LAYER_DISPLAY = {
    "editorial":   {"label": "Archive editorial",       "default_on": True,  "order": 5},
    "scholarship": {"label": "Modern scholarship",      "default_on": True,  "order": 4},
    "traditional": {"label": "Traditional commentary",  "default_on": True,  "order": 3},
    "ai":          {"label": "AI-generated (quarantined)", "default_on": False, "order": 6},
}

# Kind-specific anchor patterns. The URN grammar uses `::` between
# components, and the number of components varies by kind:
#   tale:<text>::<n>                          (2 components)
#   chapter:<text>::<trans>::<chapter>        (3 components)
#   passage:<text>::<trans>::<pid>            (3 components)
#   range:<text>::<trans>::<start>~<end>      (3 components)
ANCHOR_PATTERNS = {
    "tale":    re.compile(r"archive:tale:(?P<text>[^:]+)::(?P<id>\S+)$"),
    "passage": re.compile(r"archive:passage:(?P<text>[^:]+)::(?P<trans>[^:]+)::(?P<id>\S+)$"),
    "chapter": re.compile(r"archive:chapter:(?P<text>[^:]+)::(?P<trans>[^:]+)::(?P<id>\S+)$"),
    "range":   re.compile(r"archive:range:(?P<text>[^:]+)::(?P<trans>[^:]+)::(?P<id>\S+)$"),
}


def load_passages():
    """Return list of passages for the target tale only."""
    pf = TEXT_DIR / "passages_chalmers-vol1.json"
    data = json.loads(pf.read_text(encoding="utf-8"))
    return [p for p in data.get("passages", []) if p.get("path", [None])[0] == TARGET_TALE]


def load_meta():
    return json.loads((TEXT_DIR / "text.json").read_text(encoding="utf-8"))


def load_commentary():
    """Return flat list of all commentary records, each tagged with its file's layer."""
    all_records = []
    for layer, filename in LAYER_FILES:
        path = TEXT_DIR / filename
        if not path.exists():
            continue
        wrapper = json.loads(path.read_text(encoding="utf-8"))
        if wrapper.get("layer") != layer:
            # The non-collapse rule: filename and field must agree.
            raise SystemExit(
                f"layer mismatch: {filename} declares layer={wrapper.get('layer')!r} "
                f"but is in the {layer} file"
            )
        for rec in wrapper.get("records", []):
            rec_layer = rec.get("provenance", {}).get("layer")
            if rec_layer != layer:
                raise SystemExit(
                    f"record {rec.get('id')!r} declares layer={rec_layer!r} "
                    f"but is in the {layer} file"
                )
            rec["__file_layer"] = layer
            all_records.append(rec)
    return all_records


def parse_anchor(anchor: str) -> dict:
    """Parse an anchor URN into its components, by kind."""
    for kind, pattern in ANCHOR_PATTERNS.items():
        m = pattern.match(anchor)
        if m:
            return {"kind": kind, "raw": anchor, **m.groupdict()}
    return {"kind": None, "raw": anchor}


def build_inverse_index(records, passages):
    """Inverse index: passage_id -> list of (record, primary_anchor) for records
    that anchor here. Also handles tale-level anchors by mapping them to the
    first passage of the tale (for header attachment).
    """
    pass_ids = {p["id"] for p in passages}
    by_passage: dict[str, list[dict]] = {p["id"]: [] for p in passages}
    by_tale: list[dict] = []  # records anchored at tale-level
    by_phrase: list[tuple] = []  # records with phrase sub-locators

    for rec in records:
        for a in rec.get("anchors", []):
            parsed = parse_anchor(a["target"])
            sub = a.get("sub_locator")
            kind = parsed.get("kind")
            if kind == "passage":
                pid = parsed.get("id")
                if pid in by_passage:
                    by_passage[pid].append(
                        {"record": rec, "anchor": a, "parsed": parsed, "sub": sub}
                    )
            elif kind == "tale":
                # Confirm it matches our target tale
                if str(TARGET_TALE) in parsed.get("id", ""):
                    by_tale.append({"record": rec, "anchor": a, "parsed": parsed})
            # range, chapter — not exercised by prototype; left for future
    return {"by_passage": by_passage, "by_tale": by_tale}


def render_anchor_pill(anchor: dict) -> str:
    """Small monospace badge that shows the anchor URN. Demonstrates citation
    visibility — a reader who wants to know exactly what was anchored can read
    it."""
    raw = anchor.get("raw", "")
    sub = anchor.get("sub_locator")
    sub_part = ""
    if sub:
        if sub.get("type") == "phrase":
            sub_part = f' :phrase="{html.escape(sub.get("value",""))}"'
            if sub.get("nth", 1) != 1:
                sub_part += f' :nth={sub["nth"]}'
        else:
            sub_part = f' :{sub.get("type","?")}={html.escape(str(sub.get("value",""))[:30])}'
    return f'<code class="anchor-pill">{html.escape(raw)}{sub_part}</code>'


def render_record(rec, primary_anchor=None):
    """Render one commentary record as an expandable HTML block.

    The renderer never modifies the record. It composes HTML around it.
    """
    layer = rec.get("__file_layer", rec.get("provenance", {}).get("layer", "?"))
    label = LAYER_DISPLAY.get(layer, {}).get("label", layer)
    author = rec["provenance"].get("author", "(unattributed)")
    date = rec["provenance"].get("date", "")
    cats = rec.get("categories") or []
    cat_chips = " ".join(
        f'<span class="cat">{html.escape(c)}</span>' for c in cats
    ) if cats else '<span class="cat cat-none">(no categories)</span>'

    body = rec.get("body")
    if body is None:
        # Layer-3 bridge case
        target = rec.get("body_in_other_record")
        body_html = (
            '<p class="bridge-gap"><em>'
            'Traditional commentary expected here. The bridge points at '
            f'<code>{html.escape(target or "(no target)")}</code>, which is '
            'not currently in the archive. The gap is recorded honestly '
            'rather than filled.'
            '</em></p>'
        )
    else:
        body_html = f'<p>{html.escape(body)}</p>'

    ref = rec.get("reference_text", "")
    ref_html = f'<p class="ref-text"><em>{html.escape(ref)}</em></p>' if ref else ""

    proto = rec["provenance"].get("prototype_note")
    proto_html = (
        f'<p class="proto-note"><strong>Prototype note.</strong> {html.escape(proto)}</p>'
        if proto else ""
    )

    anchor_pills = []
    for a in rec.get("anchors", []):
        anchor_pills.append(render_anchor_pill(a))
    anchor_html = " ".join(anchor_pills)

    quarantine_badge = ""
    if layer == "ai":
        quarantine_badge = ' <span class="ai-badge">AI · quarantined · off by default</span>'

    rec_id = html.escape(rec.get("id", ""))

    return f'''
<details class="comment comment-{layer}" data-layer="{layer}" id="rec-{rec_id}">
  <summary>
    <span class="layer-label">{html.escape(label)}</span>{quarantine_badge}
    <span class="meta">{html.escape(author)} · {html.escape(date)}</span>
    {cat_chips}
  </summary>
  <div class="comment-body">
    {ref_html}
    {body_html}
    {proto_html}
    <p class="anchor-list">Anchored at: {anchor_html}</p>
    <p class="record-id">record id: <code>{rec_id}</code></p>
  </div>
</details>
'''


def render_passage(p, comments):
    """Render one passage with its attached commentary records.

    Critical: the passage's text field is rendered verbatim with HTML
    escaping. The renderer never modifies the passage text. The commentary
    sits in a <details> block below it, never inside it.
    """
    text = p.get("text", "")
    pid = p.get("id", "")
    comment_html = "\n".join(render_record(c["record"]) for c in comments)
    return f'''
<article class="passage" data-passage-id="{html.escape(pid)}">
  <p class="passage-text">
    <span class="passage-id">{html.escape(pid)}</span>
    {html.escape(text)}
  </p>
  {comment_html}
</article>
'''


CSS = """
:root {
  --bg:       #faf8f5;
  --fg:       #2c2c2c;
  --muted:    #8a7a6a;
  --rule:     #d8d3cc;
  --accent:   #7a5c3a;
  --reader-font:   Georgia, serif;
  --measure:  640px;
}
* { box-sizing: border-box; }
body {
  font-family: var(--reader-font);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.7;
  font-size: 18px;
  max-width: 800px;
  margin: 0 auto;
  padding: 32px;
}
h1 { font-weight: 500; letter-spacing: 0.02em; margin-bottom: 0.2rem; }
.subtitle { color: var(--muted); margin-top: 0; font-size: 0.9rem; font-style: italic; }
.controls {
  background: rgba(0,0,0,0.025);
  border: 1px solid var(--rule);
  padding: 12px 16px;
  margin: 24px 0;
  font-family: system-ui, sans-serif;
  font-size: 0.85rem;
  line-height: 1.5;
}
.controls h2 {
  font-family: var(--reader-font);
  font-size: 1rem;
  margin: 0 0 8px 0;
  color: var(--accent);
}
.controls label { display: inline-block; margin-right: 16px; cursor: pointer; }
.controls .master {
  display: block;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed var(--rule);
  font-weight: bold;
}
.controls .hint {
  display: block;
  margin-top: 8px;
  color: var(--muted);
  font-style: italic;
}

.passage { margin: 1.4rem 0; }
.passage-text {
  margin: 0;
  max-width: var(--measure);
}
.passage-id {
  display: inline-block;
  min-width: 3.5em;
  color: var(--muted);
  font-size: 0.78rem;
  font-family: system-ui, sans-serif;
  vertical-align: top;
  margin-right: 6px;
}

/* Commentary blocks — always visually distinct from primary text */
details.comment {
  margin: 8px 0 8px 3.5em;
  border-left: 3px solid var(--rule);
  padding-left: 12px;
  font-size: 0.92rem;
  font-family: system-ui, -apple-system, sans-serif;
}
details.comment summary {
  cursor: pointer;
  outline: none;
  color: var(--muted);
  list-style: none;
}
details.comment summary::-webkit-details-marker { display: none; }
details.comment summary:hover { color: var(--accent); }
.comment .layer-label {
  display: inline-block;
  font-weight: 600;
  margin-right: 8px;
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.06em;
}
.comment .meta {
  font-size: 0.78rem;
  color: var(--muted);
  margin-right: 8px;
}
.comment .cat {
  display: inline-block;
  padding: 0 6px;
  background: rgba(0,0,0,0.04);
  border-radius: 3px;
  font-size: 0.7rem;
  color: var(--muted);
  margin: 0 2px;
}
.comment .cat-none { font-style: italic; }
.comment-body {
  margin-top: 8px;
  padding: 8px 0;
  max-width: var(--measure);
}
.comment-body p { margin: 6px 0; }
.comment-body .ref-text { color: var(--muted); font-size: 0.85rem; }
.comment-body .proto-note {
  margin-top: 12px;
  padding: 8px 10px;
  background: rgba(184, 134, 11, 0.07);
  border-left: 2px solid rgba(184, 134, 11, 0.5);
  font-size: 0.82rem;
  color: #6b4f1f;
}
.comment-body .anchor-list {
  margin-top: 12px;
  font-size: 0.78rem;
  color: var(--muted);
}
.comment-body .record-id {
  margin-top: 4px;
  font-size: 0.7rem;
  color: var(--muted);
}
.anchor-pill {
  background: rgba(0,0,0,0.04);
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 0.78rem;
}

/* Per-layer visual signatures — each layer carries its own register. */
.comment-editorial   { border-left-color: rgba(122, 92, 58, 0.35); }
.comment-editorial summary .layer-label { color: rgba(122, 92, 58, 0.85); }

.comment-scholarship { border-left-color: rgba(40, 80, 120, 0.4); }
.comment-scholarship summary .layer-label { color: rgba(40, 80, 120, 0.85); }

.comment-traditional { border-left-color: rgba(120, 60, 40, 0.4); }
.comment-traditional summary .layer-label { color: rgba(120, 60, 40, 0.85); }
.bridge-gap {
  padding: 8px 10px;
  background: rgba(120, 60, 40, 0.05);
  border-left: 1px dashed rgba(120, 60, 40, 0.35);
  color: rgba(80, 40, 25, 0.85);
}

.comment-ai {
  border-left-color: rgba(180, 120, 180, 0.5);
  background: rgba(180, 120, 180, 0.03);
}
.comment-ai summary .layer-label { color: rgba(140, 70, 140, 0.95); }
.ai-badge {
  display: inline-block;
  background: rgba(180, 120, 180, 0.15);
  color: rgba(120, 50, 120, 0.95);
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.72rem;
  font-weight: 600;
  margin-right: 8px;
}

/* Toggle visibility: when body has layer-off-<X>, hide that layer's records. */
body.layer-off-editorial   .comment-editorial   { display: none; }
body.layer-off-scholarship .comment-scholarship { display: none; }
body.layer-off-traditional .comment-traditional { display: none; }
body.layer-off-ai          .comment-ai          { display: none; }

/* Bare canon: hide every commentary layer in one move. */
body.bare-canon .comment { display: none; }
"""

JS = """
function toggleLayer(layer, on) {
  document.body.classList.toggle('layer-off-' + layer, !on);
}
function toggleBareCanon(on) {
  document.body.classList.toggle('bare-canon', on);
  // Disable individual toggles visually while bare-canon is on
  document.querySelectorAll('.layer-toggle').forEach(el => {
    el.disabled = on;
  });
}
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.layer-toggle').forEach(cb => {
    cb.addEventListener('change', function() {
      toggleLayer(cb.dataset.layer, cb.checked);
    });
  });
  document.getElementById('master-bare-canon').addEventListener('change', function(e) {
    toggleBareCanon(e.target.checked);
  });
});
"""


def render_html(meta, passages, records, by_passage, by_tale):
    title = meta.get("chapter_titles", {}).get(str(TARGET_TALE), f"Tale {TARGET_TALE}")

    # Sort layers by display order for the toggle controls
    layer_order = sorted(LAYER_DISPLAY.items(), key=lambda x: x[1]["order"])

    toggle_controls = []
    initial_classes = []
    for layer, info in layer_order:
        default = "checked" if info["default_on"] else ""
        if not info["default_on"]:
            initial_classes.append(f"layer-off-{layer}")
        toggle_controls.append(
            f'<label><input type="checkbox" class="layer-toggle" '
            f'data-layer="{layer}" {default}> {html.escape(info["label"])}</label>'
        )

    body_class = " ".join(initial_classes)

    passages_html_parts = []

    # Tale-level commentary attaches at the head
    if by_tale:
        passages_html_parts.append('<section class="tale-level-commentary">')
        passages_html_parts.append('<h2>Tale-level commentary</h2>')
        for entry in by_tale:
            passages_html_parts.append(render_record(entry["record"]))
        passages_html_parts.append('</section>')

    for p in passages:
        comments = by_passage.get(p["id"], [])
        passages_html_parts.append(render_passage(p, comments))

    passages_html = "\n".join(passages_html_parts)

    # Compute simple statistics for the prototype footer
    n_records = len(records)
    n_at_passage = sum(1 for plist in by_passage.values() for _ in plist)
    n_at_tale = len(by_tale)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)} — commentary prototype</title>
<style>{CSS}</style>
</head>
<body class="{html.escape(body_class)}">

<h1>{html.escape(title)}</h1>
<p class="subtitle">Apannaka-jataka · Cowell ed. vol. 1 · Chalmers (1895) · commentary prototype, May 2026</p>

<div class="controls">
  <h2>Layer toggles</h2>
  {' '.join(toggle_controls)}
  <label class="master">
    <input type="checkbox" id="master-bare-canon">
    <strong>Bare canon</strong> — hide every overlay; show only the primary text exactly as the integrity proof verifies it.
  </label>
  <span class="hint">
    The toggles above are independent. AI-layer is off by default per the
    quarantine rule (<code>PROVENANCE_LAYERS.md §7</code>); a reader who
    wants to see AI suggestions must opt in by toggling it on. The
    bare-canon switch overrides every other toggle and provides the
    constitutional reading-mode (<code>COMMENTARY_CONSTITUTION.md §6</code>).
  </span>
</div>

{passages_html}

<footer style="margin-top:48px;padding-top:16px;border-top:1px solid var(--rule);font-size:0.78rem;color:var(--muted);">
  <p>
    Prototype renderer · <code>05_scripts/render_commentary_prototype.py</code> ·
    {n_records} commentary records loaded ({n_at_tale} tale-level,
    {n_at_passage} passage-level anchors).
    Generated from canonical
    <code>01_library/library/texts/sacred/buddhist/jataka-chalmers-vol1/</code>;
    no canonical files were modified.
  </p>
</footer>

<script>{JS}</script>
</body>
</html>
"""


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    meta = load_meta()
    passages = load_passages()
    records = load_commentary()
    idx = build_inverse_index(records, passages)

    output_html = render_html(meta, passages, records, idx["by_passage"], idx["by_tale"])
    OUT_PATH.write_text(output_html, encoding="utf-8")

    # Bare-canon byte-equality verification: extract the primary-text
    # content from the rendered HTML and confirm it matches the canonical
    # passages exactly (modulo HTML escaping).
    rendered_texts = re.findall(
        r'<p class="passage-text">\s*<span class="passage-id">[^<]*</span>\s*([^<]*)\s*</p>',
        output_html
    )
    canonical_texts = [p["text"] for p in passages]

    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")
    print(f"  passages rendered: {len(rendered_texts)}")
    print(f"  passages canonical: {len(canonical_texts)}")
    print(f"  commentary records: {len(records)}")
    print(f"    by_tale: {len(idx['by_tale'])}")
    print(f"    by_passage anchors: {sum(len(v) for v in idx['by_passage'].values())}")

    # Bare-canon test — escape-aware comparison
    mismatches = 0
    for rendered, canon in zip(rendered_texts, canonical_texts):
        # html.escape applied during render, so reverse it to compare
        unescaped = html.unescape(rendered).strip()
        if unescaped != canon.strip():
            mismatches += 1
    if len(rendered_texts) != len(canonical_texts):
        mismatches += abs(len(rendered_texts) - len(canonical_texts))

    if mismatches == 0:
        print("  bare-canon byte-equivalence: PASS")
    else:
        print(f"  bare-canon byte-equivalence: FAIL ({mismatches} mismatches)")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
