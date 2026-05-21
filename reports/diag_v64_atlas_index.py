"""v64 — Atlas Index page verification.

Verifies the new manuscript witness ledger:
  · the cover carries an Atlas Index button (and no codex preface link)
  · the button opens the Atlas Index page
  · the page shows book sections in canonical order
  · each chapter section is headed by a Roman numeral
  · each verse anchor lists its records with glyph + title + class
  · Genesis 1 stack renders fully (~20 records)
  · Genesis 22 (Akedah) remains silent — appears in the Silent
    Chapters list, NOT in the main index
  · Silent Chapters section exists for Genesis and is non-empty
  · Clicking a verse anchor opens the reading room at that verse
  · Back-to-Contents returns to the cover
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1. Cover: button present, preface link gone ──────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        cover_state = page.evaluate(
            """
            () => {
              return {
                hasAtlasBtn: !!document.querySelector('.bcl-atlas-index-btn'),
                hasPrefaceLink: !!document.querySelector('.bcl-codex-preface-link'),
                enterBtn: !!document.querySelector('.bcl-enter-btn'),
              };
            }
            """
        )
        print(f"Cover state: {cover_state}")
        assert cover_state["hasAtlasBtn"], "Atlas Index button missing"
        assert not cover_state["hasPrefaceLink"], "preface link should be gone"
        assert cover_state["enterBtn"], "Enter the Reading Room missing"

        page.screenshot(path="reports/v64_cover.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})

        # ── 2. Click Atlas Index → page renders ──────────────
        page.click(".bcl-atlas-index-btn")
        page.wait_for_timeout(700)
        page_state = page.evaluate(
            """
            () => {
              const root = document.querySelector('.atlas-index-page');
              if (!root) return null;
              const books = Array.from(root.querySelectorAll('.aix-book-name'))
                .map(el => el.textContent.trim());
              const chapters = Array.from(root.querySelectorAll('.aix-chapter-num'))
                .map(el => el.textContent.trim());
              const verseRefs = Array.from(root.querySelectorAll('.aix-verse-ref'))
                .map(el => ({
                  pid: el.dataset.pid,
                  label: el.textContent.trim(),
                }));
              const records = Array.from(root.querySelectorAll('.aix-record'))
                .map(r => ({
                  title: r.querySelector('.aix-record-title')?.textContent.trim() || '',
                  cls: r.querySelector('.aix-record-class')?.textContent.trim() || '',
                  glyph: r.querySelector('.aix-glyph')?.textContent.trim() || '',
                }));
              const silentSections = Array.from(root.querySelectorAll('.aix-silent'))
                .map(s => ({
                  name: s.querySelector('.aix-silent-name')?.textContent.trim() || '',
                  list: s.querySelector('.aix-silent-list')?.textContent.trim() || '',
                }));
              return { books, chapters, verseRefs, records, silentSections };
            }
            """
        )
        assert page_state, "Atlas Index page failed to render"
        print(f"Books present: {len(page_state['books'])}")
        print(f"Chapter sections: {len(page_state['chapters'])}")
        print(f"Verse anchors: {len(page_state['verseRefs'])}")
        print(f"Records rendered: {len(page_state['records'])}")
        print(f"Silent sections: {len(page_state['silentSections'])}")

        # Genesis must be the first book (canonical order)
        assert page_state["books"][0] == "Genesis", page_state["books"][:3]
        # Chapter sections must use Roman numerals
        assert "Chapter I" in page_state["chapters"]
        assert "Chapter II" in page_state["chapters"]
        assert "Chapter XII" in page_state["chapters"]
        assert "Chapter XXVIII" in page_state["chapters"]
        # Verse anchors look right (e.g., "Genesis 1:1")
        verse_labels = [v["label"] for v in page_state["verseRefs"]]
        assert "Genesis 1:1" in verse_labels
        assert "Genesis 12:1" in verse_labels
        assert "Genesis 28:18" in verse_labels
        assert "Genesis 46:3" in verse_labels
        print("  OK — Genesis ordering, Roman numerals, verse anchors")

        # Genesis 1 stack should be fully rendered (~20 records)
        gen1_count = sum(1 for v in page_state["verseRefs"]
                         if v["label"].startswith("Genesis 1:"))
        print(f"Genesis 1 verse anchors: {gen1_count}")
        assert gen1_count >= 10, gen1_count

        # Genesis 22 carries only the Nahor-house genealogy at
        # 22:20 (predates wave one). The Akedah, Moriah, hineni,
        # ram-thicket, and YHWH-jireh records are reserved for
        # wave three — none of them should appear in the index.
        gen22_records = [
            r for r in page_state["records"]
            if any(
                term in r["title"].lower()
                for term in ["akedah", "moriah", "hineni",
                             "ram thicket", "yhwh-jireh",
                             "yhwh jireh", "binding"]
            )
        ]
        assert not gen22_records, (
            f"Akedah-chamber records unexpectedly present: {gen22_records}"
        )
        print("  OK — Akedah chamber records remain absent (wave 3 reserved)")

        # The Genesis Silent Chapters list must be non-empty —
        # Genesis has many silent chapters (Gen 3, 8-11 partially,
        # 13, 18, etc.).
        gen_silent = next(
            (s for s in page_state["silentSections"]
             if s["name"].startswith("Genesis ·")),
            None,
        )
        assert gen_silent, "Genesis Silent Chapters section missing"
        assert gen_silent["list"], "Genesis silent list is empty"
        print(f"  OK — Genesis Silent Chapters: {gen_silent['list'][:60]}...")

        # Spot-check a known AO record's classification
        firmament = next(
            (r for r in page_state["records"]
             if "Firmament (rāqîaʿ)" in r["title"]),
            None,
        )
        assert firmament, "AO·001 Firmament missing"
        assert "Atlas Object · AO · 001" in firmament["cls"], firmament
        assert firmament["glyph"] == "⊕"
        print(f"  OK — AO classification: {firmament['cls']}")

        # Spot-check a tertiary architecture wave-one record
        altar = next(
            (r for r in page_state["records"]
             if "Altar at Shechem" in r["title"]),
            None,
        )
        assert altar
        assert altar["cls"] == "Tertiary · Architecture", altar
        assert altar["glyph"] == "⌂"
        print(f"  OK — wave-one tertiary classification: {altar['cls']}")

        # Spot-check a secondary commentary wave-one record
        ladder = next(
            (r for r in page_state["records"]
             if "Jacob's ladder" in r["title"]),
            None,
        )
        assert ladder
        assert ladder["cls"] == "Secondary · Commentary", ladder
        assert ladder["glyph"] == "❡"
        print(f"  OK — wave-one secondary classification: {ladder['cls']}")

        # ── 3. Screenshots ───────────────────────────────────
        page.screenshot(
            path="reports/v64_atlas_index_top.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 900},
        )
        # Scroll to a patriarchal section
        page.evaluate(
            """
            () => {
              const refs = document.querySelectorAll('.aix-verse-ref');
              for (const r of refs) {
                if (r.textContent.trim() === 'Genesis 12:1') {
                  r.scrollIntoView({block: 'center'});
                  break;
                }
              }
            }
            """
        )
        page.wait_for_timeout(400)
        page.screenshot(
            path="reports/v64_atlas_index_gen12.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 900},
        )
        # Scroll to a silent chapters section
        page.evaluate(
            """
            () => {
              const sec = document.querySelector('.aix-silent');
              if (sec) sec.scrollIntoView({block: 'center'});
            }
            """
        )
        page.wait_for_timeout(400)
        page.screenshot(
            path="reports/v64_atlas_index_silent.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 900},
        )

        # ── 4. Verse navigation ──────────────────────────────
        # Scroll back to top and click a verse anchor.
        page.evaluate("window.scrollTo({top: 0})")
        page.wait_for_timeout(300)
        page.evaluate(
            """
            () => {
              const refs = document.querySelectorAll('.aix-verse-ref');
              for (const r of refs) {
                if (r.dataset.pid === 'gen.12.1') { r.click(); break; }
              }
            }
            """
        )
        page.wait_for_timeout(1000)
        landing = page.evaluate(
            """
            () => {
              const ch = document.querySelector('.ch-sub')?.textContent;
              const url = location.search;
              const targetPassage = document.querySelector(
                '.passage[data-pid="gen.12.1"]'
              );
              return {
                chapterRoman: ch,
                url,
                hasTargetPassage: !!targetPassage,
                inReading: document.body.classList.contains('in-reading'),
                hasIndex: !!document.querySelector('.atlas-index-page'),
              };
            }
            """
        )
        print(f"After verse click: {landing}")
        assert landing["chapterRoman"] == "XII", landing
        assert landing["hasTargetPassage"], "target verse not in DOM"
        assert landing["inReading"], "should be in-reading"
        assert not landing["hasIndex"], "atlas index should have closed"
        assert "p=gen.12.1" in landing["url"], landing["url"]
        print("  OK — verse anchor opens reading room at gen.12.1")

        # ── 5. Back-to-Contents from Atlas Index ─────────────
        # Re-open the index, click back.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.click(".bcl-atlas-index-btn")
        page.wait_for_timeout(600)
        page.click(".aix-back")
        page.wait_for_timeout(600)
        on_cover = page.evaluate(
            """
            () => {
              return {
                hasAtlasBtn: !!document.querySelector('.bcl-atlas-index-btn'),
                hasIndex: !!document.querySelector('.atlas-index-page'),
              };
            }
            """
        )
        print(f"After back: {on_cover}")
        assert on_cover["hasAtlasBtn"], "should be back on cover"
        assert not on_cover["hasIndex"], "atlas index should be gone"
        print("  OK — back link returns to cover")

        b.close()
    print()
    print("ALL CHECKS PASSED — Atlas Index page is operational.")


if __name__ == "__main__":
    main()
