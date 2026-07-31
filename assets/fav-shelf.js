/* fav-shelf.js — the shared Favorites shelf (Task 84).
   One piece every archive layer loads: a 38px ☆ header button that
   opens the favorites popover (title · tradition rows linking to
   covers; the ruled empty line when none). Reads da-favorites —
   richer rows {df, title, trad} written by the cover star since
   Task 84; legacy bare-df strings from Task 81 still display (the
   filename stem stands in for the title). Styles self-injected so
   standalone pages need exactly one <script>. */
(function () {
  "use strict";
  var KEY = "da-favorites";
  var root = /\/(map|shelf|hall)\//.test(location.pathname) ? "../" : "./";

  var css =
    ".fs-pop{position:fixed;z-index:90;top:74px;right:24px;width:min(340px,92vw);" +
    "background:#faf8f5;color:#2c2c2c;border:1px solid #cfc5b4;border-radius:10px;" +
    "box-shadow:0 16px 40px rgba(0,0,0,.22);padding:18px 20px 14px;" +
    "font:14px/1.55 Georgia,serif;text-align:left;}" +
    ".fs-pop .fs-rubric{display:block;text-align:center;margin-bottom:8px;" +
    "font:400 11px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;" +
    "letter-spacing:.18em;text-transform:uppercase;color:#7a5c3a;}" +
    ".fs-pop a{display:block;padding:4px 0;color:#2c2c2c;text-decoration:none;font-size:13.5px;}" +
    ".fs-pop a:hover{color:#7a5c3a;}" +
    ".fs-pop .fs-trad{color:#8a7a6a;font-style:italic;}" +
    ".fs-pop .fs-empty{font-style:italic;color:#8a7a6a;margin:2px 0 4px;}" +
    "[data-theme=\"dark\"] .fs-pop{background:#232329;color:#d4d0c8;border-color:#44444c;}" +
    "[data-theme=\"dark\"] .fs-pop .fs-rubric{color:#c4a060;}" +
    "[data-theme=\"dark\"] .fs-pop a{color:#d4d0c8;}" +
    "[data-theme=\"dark\"] .fs-pop a:hover{color:#c4a060;}" +
    "[data-theme=\"dark\"] .fs-pop .fs-trad,[data-theme=\"dark\"] .fs-pop .fs-empty{color:#918d84;}";
  var tag = document.createElement("style");
  tag.textContent = css;
  document.head.appendChild(tag);

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function rows() {
    var f = [];
    try { f = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) {}
    return f.map(function (r) {
      if (typeof r === "string") {
        return { df: r, title: r.replace(/\.json$/, ""), trad: "" };
      }
      return { df: r.df, title: r.title || r.df, trad: r.trad || "" };
    });
  }

  var pop = null;
  function shut() {
    if (pop) { pop.remove(); pop = null; }
  }
  function open(anchorBtn) {
    shut();
    pop = document.createElement("div");
    pop.className = "fs-pop";
    pop.setAttribute("role", "dialog");
    pop.setAttribute("aria-label", "Favorites");
    var f = rows();
    var html = '<span class="fs-rubric">Favorites</span>';
    if (!f.length) {
      html += '<p class="fs-empty">No favorites yet — star any text from its cover.</p>';
    } else {
      f.forEach(function (r) {
        html += '<a href="' + root + "?text=" + encodeURIComponent(r.df) + '">' +
                esc(r.title) +
                (r.trad ? '<span class="fs-trad"> · ' + esc(r.trad) + "</span>" : "") +
                "</a>";
      });
    }
    pop.innerHTML = html;
    document.body.appendChild(pop);
    if (anchorBtn && anchorBtn.getBoundingClientRect) {
      var r = anchorBtn.getBoundingClientRect();
      pop.style.top = Math.round(r.bottom + 10) + "px";
    }
  }

  function wire(btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (pop) { shut(); return; }
      open(btn);
    });
  }
  document.addEventListener("click", function (e) {
    if (pop && !pop.contains(e.target)) shut();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") shut();
  });

  window.FavShelf = { wire: wire, open: open, shut: shut };
  document.querySelectorAll("[data-fav-shelf]").forEach(wire);
})();
