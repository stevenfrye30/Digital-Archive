#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Focused regression test for the generic deep-passage routing repair.

Verifies jumpToPassage() render-forward + reliable positioning against the LOCAL
reader (03_web_app/index.html served over http). Covers: batch-1 and batch-2+
targets, dotted and colon IDs, an invalid ID, bounded batch rendering, and
post-layout position verification. Run:  python tests/test_deep_link_routing.py
Requires: playwright (chromium). Exits non-zero on any failed assertion.
"""
import functools, http.server, socketserver, threading, time, pathlib, sys
from playwright.sync_api import sync_playwright

WEB = pathlib.Path(__file__).resolve().parent.parent          # 03_web_app
PORT = 8234
BASE = f"http://127.0.0.1:{PORT}"

# (label, data_file, pid, expected_batch)  — IDs confirmed present in the data.
CASES = [
    ("colon in-window",  "sutta-nipata-sujato_sujato.json", "snp1.2:2.1",  1),
    ("colon out-window", "sutta-nipata-sujato_sujato.json", "snp1.3:22.1", 2),
    ("dotted in-window", "dhammapada-muller_muller.json",   "4.10",        1),
    ("dotted out-window","dhammapada-muller_muller.json",   "4.250",       2),
]
RENDER_BATCH = 200

# In-page probe: returns everything the assertions need for one loaded URL.
PROBE = r"""(pid)=>{
  const t = passageById(pid);
  if (!t) return {exists:false};
  const sec = String(t.path[0]);
  const list = allPassages.filter(p => !p.fm && String(p.path[0]) === sec);
  const idx = list.findIndex(p => p.id === pid);
  const total = list.length;
  const batch = Math.floor(idx / 200) + 1;
  const expectedRendered = Math.min(total, batch * 200);
  const expectedPending = total - expectedRendered;
  const el = $passages.querySelector('.passage[data-pid="' + CSS.escape(pid) + '"]');
  const rt = $reader.getBoundingClientRect();
  let centered = false, visible = false;
  if (el) {
    const r = el.getBoundingClientRect();
    visible  = r.bottom > rt.top && r.top < rt.bottom;
    const c = (r.top + r.bottom) / 2;
    centered = c >= rt.top && c <= rt.bottom;         // its centre sits in the viewport
  }
  return {
    exists: true, sectionTotal: total, idx, batch,
    urlParsed: new URL(location).searchParams.get('p') === pid,
    inDom: !!el, visible, centered,
    pending: _pendingPassages.length, expectedPending,
    docScroll: document.documentElement.scrollTop, bodyScroll: document.body.scrollTop,
    reading: document.body.classList.contains('in-reading'),
  };
}"""

def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(WEB))
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    httpd.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    time.sleep(0.4)
    failures, errors = [], []

    def check(cond, msg):
        (print(f"  PASS  {msg}") if cond else failures.append(msg) or print(f"  FAIL  {msg}"))

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 900})
        page.on("console", lambda m: errors.append(m.type + ":" + m.text[:100])
                 if m.type == "error" and "favicon" not in m.text else None)
        page.on("pageerror", lambda e: errors.append("PAGEERR:" + str(e)[:100]))

        for label, f, pid, exp_batch in CASES:
            print(f"\n[{label}] {f}?p={pid}  (expect batch {exp_batch})")
            page.goto(f"{BASE}/?text={f}&p={pid}", wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(2200)
            r = page.evaluate(PROBE, pid)
            check(r.get("exists"), "ID exists in allPassages")
            # The reader parses ?p= into a jump to that exact passage; proof is that
            # the requested id becomes the centered target below. (After landing,
            # scroll-sync rewrites ?p= to the top-visible passage — expected — so we
            # assert reading-entry here rather than a frozen URL value.)
            check(r.get("reading"), "requested PID parsed -> entered reading")
            check(r.get("batch") == exp_batch, f"target in batch {exp_batch} (got {r.get('batch')})")
            check(r.get("inDom"), "exact target entered the DOM")
            check(r.get("visible") and r.get("centered"), "target centered/visible within $reader (requested id)")
            check(r.get("docScroll") == 0 and r.get("bodyScroll") == 0, "document/body scroll unchanged (0)")
            check(r.get("pending") == r.get("expectedPending"),
                  f"only required batches rendered (pending {r.get('pending')} == {r.get('expectedPending')})")

        # Invalid ID: no crash, jumpToPassage false, reader falls to cover (not reading).
        print("\n[invalid id] dhammapada-muller_muller.json?p=4.99999")
        page.goto(f"{BASE}/?text=dhammapada-muller_muller.json&p=4.99999",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        inv = page.evaluate("""()=>({exists:!!passageById('4.99999'),
            jump:jumpToPassage('4.99999',true),
            reading:document.body.classList.contains('in-reading')})""")
        check(not inv["exists"], "invalid ID absent from data")
        check(inv["jump"] is False, "jumpToPassage returns false for invalid ID")
        check(not inv["reading"], "invalid ID shows cover (not reading)")

        # Translation switch to an out-of-window aligned Sujato passage.
        print("\n[translation switch -> out-of-window] snp1.3:22.1")
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_pli.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2200)
        page.evaluate("""()=>{const s=document.getElementById('translation-select');
            s.value='sutta-nipata-sujato_sujato.json';s.dispatchEvent(new Event('change'));}""")
        page.wait_for_timeout(2200)
        sw = page.evaluate(PROBE, "snp1.3:22.1")
        check(sw.get("inDom") and sw.get("centered"),
              "switch renders-forward + centers the out-of-window passage")

        # Manual "Load more" still works after an automatic deep jump.
        print("\n[manual Load more after deep jump]")
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_sujato.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)
        lm = page.evaluate("""()=>{const before=_pendingPassages.length;
            const b=$passages.querySelector('.load-more-btn'); if(!b) return {before,btn:false};
            b.click(); return {before, after:_pendingPassages.length, btn:true};}""")
        check(lm.get("btn") and lm["after"] < lm["before"],
              f"manual Load more renders further ({lm.get('before')} -> {lm.get('after')})")

        # 380px narrow: no horizontal overflow on a deep-linked passage.
        print("\n[narrow 380px]")
        page.set_viewport_size({"width": 380, "height": 820})
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_sujato.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)
        narrow = page.evaluate(PROBE, "snp1.3:22.1")
        hscroll = page.evaluate("()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+2")
        check(narrow.get("inDom") and narrow.get("centered"), "narrow: target centered")
        check(not hscroll, "narrow: no horizontal overflow")

        # ── Citation permanence ────────────────────────────────────────────────
        page.set_viewport_size({"width": 1280, "height": 900})
        BM = "()=>{try{return JSON.parse(localStorage.getItem('da-last')||'{}').pid||null}catch(e){return null}}"
        URLP = "()=>new URL(location).searchParams.get('p')"

        # 1) Exact-PID permanence at landing, 500 ms, 2 s — no user input, no drift.
        for label, f, pid, _exp in CASES:
            print(f"\n[permanence] {f}?p={pid}")
            page.goto(f"{BASE}/?text={f}&p={pid}", wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(300)
            check(page.evaluate(URLP) == pid, "URL == requested at landing")
            page.wait_for_timeout(500)
            check(page.evaluate(URLP) == pid, "URL == requested at +500ms (no drift)")
            page.wait_for_timeout(1500)
            r = page.evaluate(PROBE, pid)
            check(page.evaluate(URLP) == pid, "URL == requested at +2s (no drift)")
            check(page.evaluate(BM) == pid, "bookmark == requested at +2s")
            check(r.get("centered"), "requested still centered at +2s")

        # 2) Genuine user scroll releases protection; URL/bookmark then track position.
        print("\n[user-scroll release]")
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_sujato.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        check(page.evaluate(URLP) == "snp1.3:22.1", "protected before user scroll")
        page.mouse.move(640, 450)
        page.mouse.wheel(0, 350)                       # real wheel event -> release + scroll
        page.wait_for_timeout(700)
        u1 = page.evaluate(URLP)
        check(u1 != "snp1.3:22.1" and page.evaluate("()=>_citationPid") is None,
              f"released + URL tracks new position ({u1})")
        check(page.evaluate(BM) == u1, "bookmark tracks new position after release")
        page.mouse.wheel(0, 350)                       # keep scrolling -> keeps tracking
        page.wait_for_timeout(700)
        check(page.evaluate(URLP) not in ("snp1.3:22.1", u1), "continues tracking further user scroll")

        # 3) Translation-switch permanence: aligned PID retained, no drift.
        print("\n[translation-switch permanence]")
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_sujato.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        for target in ("sutta-nipata-sujato_pli.json", "sutta-nipata-sujato_sujato.json"):
            page.evaluate("""(v)=>{const s=document.getElementById('translation-select');
                s.value=v;s.dispatchEvent(new Event('change'));}""", target)
            page.wait_for_timeout(1800)
            a = page.evaluate(URLP)
            page.wait_for_timeout(1500)
            check(a and page.evaluate(URLP) == a and page.evaluate("()=>_citationPid") == a,
                  f"switch -> {target.split('_')[-1]}: aligned PID {a} retained, no drift")

        # 4) State cleanup: superseded jump, invalid id, and opening Contents.
        print("\n[state cleanup]")
        page.goto(f"{BASE}/?text=sutta-nipata-sujato_sujato.json&p=snp1.3:22.1",
                  wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        sup = page.evaluate("()=>{jumpToPassage('snp1.2:2.1',true);return _citationPid;}")
        check(sup == "snp1.2:2.1", "superseded jump re-arms to the new PID")
        inv = page.evaluate("()=>{jumpToPassage('snp9.9:9.9',true);return _citationPid;}")
        check(inv is None, "invalid jump clears protection")
        page.evaluate("()=>openWitnessContents('sutta-nipata-sujato')")
        page.wait_for_timeout(600)
        check(page.evaluate("()=>_citationPid") is None, "opening Contents clears protection")

        browser.close()
    httpd.shutdown()

    check(not errors, f"zero console/page errors ({errors[:4]})")
    print("\n" + ("ALL PASSED" if not failures else f"{len(failures)} FAILURE(S): {failures}"))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
