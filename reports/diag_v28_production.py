"""v28 — compare LOCAL vs PRODUCTION folio rendering."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from playwright.sync_api import sync_playwright


PROD_URL = "https://stevenfrye30.github.io/Digital-Archive/?text=bible_kjv.json&p=gen.1.1"
LOCAL_URL = "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1"


def probe(page, label, click_companion=True):
    """Returns DOM + asset state."""
    if click_companion:
        try:
            page.click("#companion-toggle", timeout=5000)
            page.wait_for_timeout(900)
        except Exception as e:
            print(f"  [WARN] couldn't click companion-toggle: {e}")
    return page.evaluate(
        """
      () => {
        const ret = {
          url: location.href,
          bodyClasses: Array.from(document.body.classList),
          markers: document.querySelectorAll('.cr-folio-marker').length,
          clusters: document.querySelectorAll('.cr-folio-cluster').length,
          folioColumns: document.querySelectorAll('.folio-column').length,
          chapterSpread: !!document.querySelector('.chapter-spread'),
          companionToggleExists: !!document.getElementById('companion-toggle'),
          companionToggleText: document.getElementById('companion-toggle')?.textContent,
          inReading: document.body.classList.contains('in-reading'),
          chapterRoom: document.body.classList.contains('chapter-room'),
          companionMode: document.body.classList.contains('companion-mode'),
          colsSingle: document.body.classList.contains('cols-single'),
          // Data state
          dataRecordCount: (typeof currentData !== 'undefined' &&
                            currentData?.genealogy)
                           ? currentData.genealogy.length : null,
          gen1RecordsInData: (typeof currentData !== 'undefined' &&
                              currentData?.genealogy)
            ? currentData.genealogy.filter(r => {
                const a = r.anchors?.[0]?.target;
                return a && a.split('::').pop().startsWith('gen.1.');
              }).length : null,
          // Currently loaded text
          currentTextId: typeof currentEntry !== 'undefined' ? currentEntry?.text_id : null,
          currentBook: typeof currentBook !== 'undefined' ? currentBook : null,
          // Visual state of one marker (if any)
          firstMarkerCSS: (() => {
            const m = document.querySelector('.cr-folio-marker');
            if (!m) return null;
            const cs = getComputedStyle(m);
            const before = getComputedStyle(m, '::before');
            const r = m.getBoundingClientRect();
            return {
              display: cs.display,
              visibility: cs.visibility,
              opacity: cs.opacity,
              dataKind: m.dataset.kind,
              beforeContent: before.content,
              rect: r.toJSON(),
            };
          })(),
          firstFolioColumnCSS: (() => {
            const f = document.querySelector('.folio-column');
            if (!f) return null;
            const cs = getComputedStyle(f);
            return {
              display: cs.display,
              visibility: cs.visibility,
              opacity: cs.opacity,
              width: cs.width,
              gridColumn: cs.gridColumn,
            };
          })(),
          // JS function presence
          hasRenderChapterRoomFolio: typeof _renderChapterRoomFolio === 'function',
          hasRenderFolioMarker: typeof _renderFolioMarker === 'function',
          hasPositionFolioEntries: typeof _positionFolioEntries === 'function',
          hasPositionMarkerPlaque: typeof _positionMarkerPlaque === 'function',
        };
        return ret;
      }
        """
    )


def fetch_text(page, url):
    """Use page context to fetch — same cache behavior as the loader."""
    return page.evaluate(
        f"""
      async () => {{
        const tryUrl = async (u) => {{
          const r = await fetch(u, {{ cache: 'no-store' }});
          if (!r.ok) return {{ url: u, ok: false, status: r.status }};
          const buf = await r.arrayBuffer();
          return {{ url: u, ok: true, status: r.status, byteLength: buf.byteLength }};
        }};
        const gz = await tryUrl('{url}.gz');
        const raw = await tryUrl('{url}');
        return {{ gz, raw }};
      }}
        """
    )


def show(label, info):
    print(f"\n┌── {label} " + "─" * (60 - len(label)))
    for k, v in info.items():
        if isinstance(v, dict):
            print(f"│ {k}:")
            for kk, vv in v.items():
                print(f"│   {kk}: {vv}")
        else:
            print(f"│ {k}: {v}")
    print("└" + "─" * 65)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ── LOCAL ────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("LOCAL")
        print("=" * 60)
        local_ctx = b.new_context(viewport={"width": 1440, "height": 900})
        local_page = local_ctx.new_page()
        local_console = []
        local_page.on("console", lambda m: local_console.append(f"[{m.type}] {m.text}"))
        local_page.on("pageerror", lambda e: local_console.append(f"[PAGEERROR] {e}"))
        local_page.goto(LOCAL_URL, wait_until="networkidle")
        local_page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        local_page.wait_for_timeout(800)
        local_state = probe(local_page, "local")
        show("LOCAL state", local_state)
        local_fetches = fetch_text(local_page, "/data/bible_kjv.json")
        print(f"\nLOCAL fetch /data/bible_kjv.json")
        print(f"  .gz: {local_fetches['gz']}")
        print(f"  raw: {local_fetches['raw']}")
        if local_console:
            print("LOCAL console messages:")
            for m in local_console[-20:]:
                print(f"  {m}")
        local_ctx.close()

        # ── PRODUCTION ───────────────────────────────────────
        print("\n" + "=" * 60)
        print("PRODUCTION")
        print("=" * 60)
        prod_ctx = b.new_context(
            viewport={"width": 1440, "height": 900},
            # Don't bring caches with us
        )
        prod_page = prod_ctx.new_page()
        prod_console = []
        prod_page.on("console", lambda m: prod_console.append(f"[{m.type}] {m.text}"))
        prod_page.on("pageerror", lambda e: prod_console.append(f"[PAGEERROR] {e}"))
        try:
            prod_page.goto(PROD_URL, wait_until="networkidle", timeout=30000)
            try:
                prod_page.wait_for_function(
                    "typeof currentData === 'object' && currentData && currentData.passages",
                    timeout=20000,
                )
            except Exception as e:
                print(f"[WARN] currentData not ready: {e}")
            prod_page.wait_for_timeout(1500)
            prod_state = probe(prod_page, "production")
            show("PRODUCTION state", prod_state)
            # Use ABSOLUTE fetch URLs on production
            base = "https://stevenfrye30.github.io/Digital-Archive/data/bible_kjv.json"
            prod_fetches = fetch_text(prod_page, base)
            print(f"\nPRODUCTION fetch {base}")
            print(f"  .gz: {prod_fetches['gz']}")
            print(f"  raw: {prod_fetches['raw']}")

            # If gz served, fetch and inspect record count
            if prod_fetches["gz"].get("ok"):
                # Get gz bytes via JS DecompressionStream
                rec_count = prod_page.evaluate(
                    """
                  async () => {
                    try {
                      const r = await fetch('https://stevenfrye30.github.io/Digital-Archive/data/bible_kjv.json.gz', { cache: 'no-store' });
                      const ds = new DecompressionStream('gzip');
                      const text = await new Response(r.body.pipeThrough(ds)).text();
                      const data = JSON.parse(text);
                      const gen1 = (data.genealogy || []).filter(rec => {
                        const a = rec.anchors?.[0]?.target;
                        return a && a.split('::').pop().startsWith('gen.1.');
                      });
                      return {
                        totalRecords: (data.genealogy || []).length,
                        gen1Records: gen1.length,
                        gen1Titles: gen1.map(r => r.title).slice(0, 5),
                      };
                    } catch (e) {
                      return { error: String(e) };
                    }
                  }
                    """
                )
                print(f"\nPRODUCTION data file content:")
                print(f"  totalRecords: {rec_count.get('totalRecords')}")
                print(f"  gen.1 records: {rec_count.get('gen1Records')}")
                print(f"  first 5 titles: {rec_count.get('gen1Titles')}")

            # Asset-version probe: get index.html as served by production
            asset_info = prod_page.evaluate(
                """
              async () => {
                const r = await fetch('https://stevenfrye30.github.io/Digital-Archive/index.html', { cache: 'no-store' });
                const txt = await r.text();
                return {
                  htmlLength: txt.length,
                  hasMarkerCss: txt.includes('cr-folio-marker'),
                  hasClusterCss: txt.includes('cr-folio-cluster'),
                  hasNewKinds: txt.includes('cosmology') && txt.includes('reception-history'),
                  hasPositionMarkerPlaque: txt.includes('_positionMarkerPlaque'),
                  hasGen1Calibration: txt.includes('chapter-spread'),
                  etag: r.headers.get('etag'),
                  lastModified: r.headers.get('last-modified'),
                };
              }
                """
            )
            print(f"\nPRODUCTION index.html asset:")
            for k, v in asset_info.items():
                print(f"  {k}: {v}")

            prod_page.screenshot(path="reports/v28_production.png")
        except Exception as e:
            print(f"[ERROR] Production probe failed: {e}")

        if prod_console:
            print("\nPRODUCTION console messages:")
            for m in prod_console[-30:]:
                print(f"  {m}")
        prod_ctx.close()

        b.close()


if __name__ == "__main__":
    main()
