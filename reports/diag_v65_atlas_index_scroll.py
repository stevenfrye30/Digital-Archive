"""v65 — Atlas Index scroll fix.

Regression that surfaced after v64: the Atlas Index page rendered
correctly but the reader container kept its inline overflow:hidden
from the welcome/cover scaffolding, so the index was clipped at the
first viewport. Long content (Genesis 12, 28, 46, Exodus, Silent
Chapters) was unreachable.

This diagnostic verifies:
  · the reader column (#reader) is now the scroll surface
  · its scrollHeight exceeds the viewport
  · programmatic scrolling to the bottom is possible
  · Silent Chapters and Revelation are reachable
  · back-to-contents still works after scrolling
  · the reading room can still be entered afterward
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)

        # Open the Atlas Index
        page.click(".bcl-atlas-index-btn")
        page.wait_for_timeout(800)

        # ── 1. Reader is the scroll surface, content is long ─
        scroll_state = page.evaluate(
            """
            () => {
              const reader = document.getElementById('reader');
              const cs = getComputedStyle(reader);
              const page = document.querySelector('.atlas-index-page');
              return {
                readerOverflowY: cs.overflowY,
                inlineOverflow: reader.style.overflow,
                readerScrollHeight: reader.scrollHeight,
                readerClientHeight: reader.clientHeight,
                pagePresent: !!page,
                pageHeight: page ? page.getBoundingClientRect().height : 0,
              };
            }
            """
        )
        print(f"Scroll state at open: {scroll_state}")
        assert scroll_state["pagePresent"], "atlas index missing"
        # CSS rule is overflow-y: auto; the inline hidden must
        # have been cleared.
        assert scroll_state["readerOverflowY"] == "auto", (
            f"reader overflow-y = {scroll_state['readerOverflowY']}"
        )
        assert scroll_state["inlineOverflow"] in ("", "auto", "visible"), (
            f"inline overflow still set: {scroll_state['inlineOverflow']!r}"
        )
        # Content must exceed viewport so scrolling is meaningful.
        assert scroll_state["readerScrollHeight"] > scroll_state["readerClientHeight"] + 200, (
            f"content not tall enough: scroll={scroll_state['readerScrollHeight']} "
            f"client={scroll_state['readerClientHeight']}"
        )
        print("  OK — reader scrolls, content exceeds viewport\n")

        # ── 2. Programmatic scroll to bottom; bottom content present
        page.evaluate(
            """
            () => {
              const r = document.getElementById('reader');
              r.scrollTop = r.scrollHeight;
            }
            """
        )
        page.wait_for_timeout(500)
        bottom_state = page.evaluate(
            """
            () => {
              const r = document.getElementById('reader');
              return {
                scrollTop: r.scrollTop,
                scrollHeight: r.scrollHeight,
                clientHeight: r.clientHeight,
                nearBottom: r.scrollTop + r.clientHeight >= r.scrollHeight - 4,
                lastBookName: (() => {
                  const books = document.querySelectorAll('.aix-book-name');
                  return books.length ? books[books.length - 1].textContent.trim() : null;
                })(),
                silentSectionsCount: document.querySelectorAll('.aix-silent').length,
              };
            }
            """
        )
        print(f"After scroll-to-bottom: {bottom_state}")
        assert bottom_state["nearBottom"], "could not scroll to bottom"
        # The data has 20 books; the last one in canonical order
        # that carries records is Revelation.
        assert bottom_state["lastBookName"] == "Revelation", (
            f"last book = {bottom_state['lastBookName']!r}"
        )
        assert bottom_state["silentSectionsCount"] >= 5
        print("  OK — bottom reachable, Revelation present, silent sections rendered\n")

        # ── 3. Silent Chapters section is reachable + visible ─
        silent_reachable = page.evaluate(
            """
            () => {
              const sec = document.querySelector('.aix-silent');
              if (!sec) return null;
              sec.scrollIntoView({block: 'center'});
              const rect = sec.getBoundingClientRect();
              return {
                name: sec.querySelector('.aix-silent-name')?.textContent.trim(),
                list: sec.querySelector('.aix-silent-list')?.textContent.trim(),
                top: rect.top,
                bottom: rect.bottom,
                inViewport: rect.top >= 0 && rect.bottom <= window.innerHeight,
              };
            }
            """
        )
        print(f"Silent section: {silent_reachable}")
        assert silent_reachable["name"].startswith("Genesis ·")
        assert "VIII" in silent_reachable["list"]
        assert silent_reachable["inViewport"]
        page.screenshot(
            path="reports/v65_atlas_silent_visible.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 900},
        )
        print("  OK — Silent Chapters reachable and within viewport\n")

        # ── 4. Revelation reachable (final canonical book) ───
        page.evaluate(
            """
            () => {
              const all = document.querySelectorAll('.aix-book-name');
              const last = all[all.length - 1];
              if (last) last.scrollIntoView({block: 'start'});
            }
            """
        )
        page.wait_for_timeout(400)
        page.screenshot(
            path="reports/v65_atlas_revelation_visible.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 900},
        )

        # ── 5. Back to Contents after scrolling ──────────────
        # Scroll all the way down first to ensure the back button
        # still works from a deep scroll position.
        page.evaluate("document.getElementById('reader').scrollTop = 99999")
        page.wait_for_timeout(300)
        # The back button is absolute-positioned in the page header;
        # scroll back to the top to click it (or click via JS).
        page.evaluate(
            "() => document.getElementById('aix-back-btn').click()"
        )
        page.wait_for_timeout(700)
        cover_state = page.evaluate(
            """
            () => ({
              hasIndex: !!document.querySelector('.atlas-index-page'),
              hasCover: !!document.querySelector('.bible-cover-layout'),
              hasAtlasBtn: !!document.querySelector('.bcl-atlas-index-btn'),
            })
            """
        )
        print(f"After back-to-contents: {cover_state}")
        assert not cover_state["hasIndex"]
        assert cover_state["hasCover"]
        assert cover_state["hasAtlasBtn"]
        print("  OK — back-to-contents from deep scroll position\n")

        # ── 6. Enter Reading Room still works afterward ──────
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(900)
        reading_state = page.evaluate(
            """
            () => ({
              inReading: document.body.classList.contains('in-reading'),
              chapterRoman: document.querySelector('.ch-sub')?.textContent || null,
              firstPassage: !!document.querySelector('.passage'),
            })
            """
        )
        print(f"Reading room after Atlas Index round-trip: {reading_state}")
        assert reading_state["inReading"]
        assert reading_state["chapterRoman"] == "I"
        assert reading_state["firstPassage"]
        print("  OK — Reading Room still works\n")

        # ── 7. Re-open Atlas Index from cover (round-trip) ───
        page.click("#ctrl-contents")
        page.wait_for_timeout(700)
        page.click(".bcl-atlas-index-btn")
        page.wait_for_timeout(700)
        roundtrip = page.evaluate(
            """
            () => {
              const r = document.getElementById('reader');
              return {
                hasIndex: !!document.querySelector('.atlas-index-page'),
                scrollTop: r.scrollTop,
                scrollHeight: r.scrollHeight,
                clientHeight: r.clientHeight,
                inlineOverflow: r.style.overflow,
              };
            }
            """
        )
        print(f"Round-trip Atlas Index: {roundtrip}")
        assert roundtrip["hasIndex"]
        assert roundtrip["scrollTop"] == 0
        assert roundtrip["scrollHeight"] > roundtrip["clientHeight"] + 200
        assert roundtrip["inlineOverflow"] in ("", "auto", "visible")
        print("  OK — Atlas Index opens scrollable again after round-trip\n")

        b.close()
    print("ALL CHECKS PASSED — Atlas Index scrolls as a long manuscript appendix.")


if __name__ == "__main__":
    main()
