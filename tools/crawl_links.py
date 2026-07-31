#!/usr/bin/env python3
"""crawl_links.py — the full deep-link sweep (Task 60; lane 5 of 5).

The route validator models the surfaces it knows; this crawler walks
what actually LINKS: every href/src on every public HTML surface, plus
every data-minted route (?text= from the index, bindings read urls,
doors/trad2map/df2map/chip_index map slugs, stewardship pages named in
text data). Classes reported:

  DEAD          internal link whose target file does not exist
  BROKEN-ANCHOR #fragment with no matching id in the target page
  BROKEN-PARAM  ?text= route whose data file is absent
  STUB-FIRSTHOP a live (non-stub) page linking onto a redirect stub —
                first hops must never land a stub (the Task 42 rule)
  ORPHAN        an HTML surface no live page links to (reported, never
                deleted — the steward rules on orphans); redirect stubs
                are permanence artifacts, listed separately, not orphans
  EXTERNAL      deduped external URLs (report-only; checked with --net)

Report-only by default; exits 1 when a mechanical class (DEAD /
BROKEN-ANCHOR / BROKEN-PARAM / STUB-FIRSTHOP) is non-empty, so it can
sit beside the batteries.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

WEB = Path(__file__).resolve().parent.parent

# (?<![\w.]) keeps JS property access (location.href = ...) out of
# the markup-attribute match — JSNAV owns those
HREF = re.compile(r"""(?<![\w.])(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
# complete assignments only — a concatenated fragment ('map/' + slug)
# is not a link
JSNAV = re.compile(r"""location\.(?:href|replace)\s*[=(]\s*["']([^"']+)["']\s*[;)
]""")
ID_ATTR = re.compile(r"""id\s*=\s*["']([^"']+)["']""")


def is_stub(text: str) -> bool:
    return 'http-equiv="refresh"' in text


def norm_target(base: Path, link: str) -> tuple[str | None, str, str]:
    """→ (kind, resolved_relpath_or_url, fragment). kind: int/ext/skip."""
    link = link.strip()
    if not link or link.startswith(("javascript:", "mailto:", "data:")):
        return ("skip", link, "")
    if "${" in link:
        # a JS template literal inside <script> source, not markup
        return ("skip", link, "")
    u = urlparse(link)
    frag = u.fragment
    if u.scheme in ("http", "https"):
        # internal-absolute forms resolve internally
        if u.netloc == "stevenfrye30.github.io" and u.path.startswith("/Digital-Archive"):
            path = u.path[len("/Digital-Archive"):] or "/"
        else:
            return ("ext", link.split("#")[0], frag)
    else:
        path = u.path
    if path.startswith("/Digital-Archive"):
        path = path[len("/Digital-Archive"):] or "/"
    if path.startswith("/"):
        resolved = (WEB / path.lstrip("/")).resolve()
    elif path == "":
        resolved = (WEB / base).resolve() if frag else (WEB / base).resolve()
    else:
        resolved = ((WEB / base).parent / unquote(path)).resolve()
    if resolved.is_dir():
        resolved = resolved / "index.html"
    try:
        rel = resolved.relative_to(WEB).as_posix()
    except ValueError:
        return ("ext", link.split("#")[0], frag)
    return ("int", rel + (("?" + u.query) if u.query else ""), frag)


def main() -> int:
    net = "--net" in sys.argv
    pages = {}
    for p in glob.glob(str(WEB / "**/*.html"), recursive=True):
        rel = Path(p).relative_to(WEB).as_posix()
        if rel.startswith(".git"):
            continue
        pages[rel] = Path(p).read_text(encoding="utf-8", errors="replace")
    stubs = {r for r, t in pages.items() if is_stub(t)}
    ids = {r: set(ID_ATTR.findall(t)) for r, t in pages.items()}

    ix = json.loads((WEB / "data/_generated/index.json").read_text(encoding="utf-8"))["texts"]
    public_dfs = {e["data_file"] for e in ix if e.get("data_file") and not e.get("restricted")}

    def df_exists(df: str) -> bool:
        return (WEB / "data" / df).is_file() or (WEB / "data" / (df + ".gz")).is_file()

    dead, broken_anchor, broken_param, stub_hop = [], [], [], []
    externals = set()
    inbound = defaultdict(set)

    def check_int(src: str, rel_q: str, frag: str) -> None:
        rel, _, query = rel_q.partition("?")
        target = WEB / rel
        if not target.is_file():
            dead.append((src, rel_q))
            return
        inbound[rel].add(src)
        if rel in stubs and src not in stubs:
            stub_hop.append((src, rel))
        if query:
            m = re.search(r"(?:^|&)text=([^&]+)", query)
            if m and not df_exists(unquote(m.group(1))):
                broken_param.append((src, rel_q))
        if frag and rel in ids and frag not in ids[rel]:
            broken_anchor.append((src, rel_q + "#" + frag))

    # 1 — every href/src + inline JS navigation on every HTML surface
    for rel, text in pages.items():
        for link in HREF.findall(text) + JSNAV.findall(text):
            kind, tgt, frag = norm_target(Path(rel), link)
            if kind == "int":
                check_int(rel, tgt, frag)
            elif kind == "ext":
                externals.add(tgt)

    # 2 — data-minted routes
    for df in sorted(public_dfs):          # the reader's ?text= routes
        if not df_exists(df):
            broken_param.append(("data/_generated/index.json", "?text=" + df))
    for bf in sorted((WEB / "maps").glob("*/bindings.json")):
        b = json.loads(bf.read_text(encoding="utf-8"))
        src = bf.relative_to(WEB).as_posix()
        for ch in b["chips"]:
            for r in (ch.get("read") or []):
                m = re.search(r"text=([^&]+)", r.get("url", ""))
                if m and not df_exists(unquote(m.group(1))):
                    broken_param.append((src, r["url"]))
    for jf, field in (("maps/doors.json", None), ("maps/trad2map.json", "trad2map"),
                      ("maps/df2map.json", "df2map")):
        fp = WEB / jf
        if not fp.is_file():
            continue
        j = json.loads(fp.read_text(encoding="utf-8"))
        slugs = set()
        if field is None:
            for d in j.get("doors", []):
                if d.get("tradition"):
                    slugs.add(d["tradition"])
        elif field == "trad2map":
            slugs.update(j["trad2map"].values())
        else:
            slugs.update(v[0] for v in j["df2map"].values())
        for s in sorted(slugs):
            rel = f"map/{s}.html"
            if not (WEB / rel).is_file():
                dead.append((jf, rel))
            else:
                inbound[rel].add(jf)
    ci = WEB / "maps/chip_index.json"
    if ci.is_file():
        for r in json.loads(ci.read_text(encoding="utf-8"))["chips"]:
            rel = f"map/{r['m']}.html"
            if not (WEB / rel).is_file():
                dead.append(("maps/chip_index.json", rel))
    # stewardship pages named inside text data
    for e in ix:
        df = e.get("data_file")
        if not df or e.get("restricted") or not df_exists(df):
            continue
        p = WEB / "data" / df
        if p.is_file():
            t = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'"stewardship_history_url"\s*:\s*"([^"]+)"', t)
            if m:
                kind, tgt, frag = norm_target(Path("index.html"), m.group(1))
                if kind == "int":
                    check_int("data/" + df, tgt, frag)

    # 3 — orphans (stubs excluded: permanence artifacts by design)
    orphans = sorted(r for r in pages
                     if r not in inbound and r not in stubs and r != "index.html")

    # 4 — externals (checked only with --net)
    ext_fail = []
    if net:
        import urllib.request
        for u in sorted(externals):
            try:
                req = urllib.request.Request(u, method="HEAD",
                                             headers={"User-Agent": "da-linkcheck"})
                urllib.request.urlopen(req, timeout=8)
            except Exception as ex:
                ext_fail.append((u, str(ex)[:60]))

    dead = sorted(set(dead))
    broken_param = sorted(set(broken_param))
    print(f"pages crawled: {len(pages)} ({len(stubs)} redirect stubs) · "
          f"data routes: {len(public_dfs)} texts")
    print(f"DEAD: {len(dead)}")
    for s, t in dead:
        print(f"  {s} -> {t}")
    print(f"BROKEN-ANCHOR: {len(broken_anchor)}")
    for s, t in broken_anchor:
        print(f"  {s} -> {t}")
    print(f"BROKEN-PARAM: {len(broken_param)}")
    for s, t in broken_param:
        print(f"  {s} -> {t}")
    print(f"STUB-FIRSTHOP: {len(stub_hop)}")
    for s, t in stub_hop:
        print(f"  {s} -> {t}")
    print(f"ORPHANS (report-only; steward rules): {len(orphans)}")
    for r in orphans:
        print(f"  {r}")
    print(f"EXTERNAL (deduped): {len(externals)}" + ("" if net else "  [--net to check]"))
    for u, err in ext_fail:
        print(f"  FAIL {u} ({err})")
    mech = len(dead) + len(broken_anchor) + len(broken_param) + len(stub_hop)
    print("MECHANICAL BREAKAGE:", mech)
    return 1 if mech else 0


if __name__ == "__main__":
    sys.exit(main())
