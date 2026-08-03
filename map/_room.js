(function () {
  var SLUG = document.body.getAttribute('data-map');
  if (!SLUG) return;
  function norm(s) {
    return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
            .replace(/^the\s+/, '').replace(/[^a-z0-9]+/g, '');
  }
  function nid(s) {
    s = (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    s = s.split('\u2014')[0].split(' \u00b7 ')[0].split(' (')[0];
    return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  function dupLabel(r) {
    // a chooser label that merely repeats translator+year is
    // suppressed (37 dress fix 4: 'Hume, 1921 \u2014 Hume, 1921')
    if (!r.label) return '';
    var ty = ((r.translator || '') + (r.year ? ', ' + r.year : '')).toLowerCase().replace(/\s+/g, ' ').trim();
    var lb = String(r.label).toLowerCase().replace(/\s+/g, ' ').trim();
    return lb === ty ? '' : ' \u2014 ' + r.label;
  }
  // Task 119 — the lens is retired. `da-map-lens` is no longer read or
  // written, and ?lens= is no longer honoured: a stored 'rights' would
  // otherwise put returning readers into a mode that no longer exists.
  // The one stale key is cleared so nothing outlives the toggle.
  try { localStorage.removeItem('da-map-lens'); } catch (e) {}
  var params = new URLSearchParams(location.search);
  // Task 59 — search deep-link: ?chip=<norm> scrolls to the chip and
  // flashes it once (no lens change; the entrance is the one finder).
  var chipSought = params.get('chip');
  if (chipSought) {
    setTimeout(function () {
      var target = null, loose = null;
      document.querySelectorAll('section[id] .chip, section[id] .su, section[id] .tc')
        .forEach(function (el) {
          if (target) return;
          var nmEl = el.querySelector('.nm') || el.querySelector('.tl') || el;
          var t = norm((nmEl.textContent || '').trim());
          if (t === chipSought) { target = el; return; }
          // page chips may carry ordinals the structure name lacks
          // ('9 Poṭṭhapāda' vs 'Poṭṭhapāda') — containment fallback
          if (!loose && chipSought.length >= 4 && t.indexOf(chipSought) >= 0) loose = el;
        });
      target = target || loose;
      if (!target) return;
      // the chip may live behind a sub-tradition tab (the 40a views) —
      // activate its view first, then measure and scroll
      var vp = target.closest('section.view[id^="view-"]');
      if (vp && getComputedStyle(vp).display === 'none') {
        var vbtn = document.querySelector('button[data-view="' + vp.id.replace(/^view-/, '') + '"]');
        if (vbtn) vbtn.click();
      }
      setTimeout(function () {
        var r = target.getBoundingClientRect();
        window.scrollTo({ top: r.top + window.pageYOffset - 160, behavior: 'smooth' });
        target.classList.add('chip-sought');
        setTimeout(function () { target.classList.remove('chip-sought'); }, 3400);
      }, 200);
    }, 400);
  }
  var B = null, PROV = {};
  // 36a race guard: a chip clicked before these resolve must never
  // render a false not-held — open() waits on this promise.
  var _ready = Promise.all([
    (window.__bindingsP || (window.__bindingsP = fetch('../maps/' + SLUG + '/bindings.json').then(function (r) { return r.json(); })))
      .then(function (j) { B = {}; j.chips.forEach(function (c) { B[c.zone + '||' + norm(c.chip)] = c; }); })
      .catch(function () { B = {}; }),
    fetch('../maps/' + SLUG + '/provenance.json').then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.nodes) PROV = j.nodes; }).catch(function () {})
  ]);

  // toggle pills — the reader's Reading/Interactive grammar
  // Task 37: the reception section (Task 32's inline layer) becomes an
  // OVERLAY — find it now; when absent the Reception toggle is omitted.
  var recSec = document.querySelector('section[id$="-reception"]');
  // Task 119 — the STRUCTURE / RIGHTS toggle and its banner are gone.
  // What survives is the HELD-EDITIONS SHEET, which the retired toggle
  // happened to carry as a third 'held' lens value: setLens('held')
  // was what opened it. That was the one real trap in this merge —
  // deleting the lens naively would have taken the sheet with it — so
  // the sheet now owns its own open/close and no longer pretends to be
  // a view. The sheet is a surface over the page, not a mode of it.
  var sheetOpen = false;
  function showSheet() { sheetOpen = true; close(); openOverlay(); }
  function hideSheet() { sheetOpen = false; closeOverlay(); }
  function toggleSheet() { if (sheetOpen) hideSheet(); else showSheet(); }

  // ── Task 37: the two content overlays (Held editions · Reception) ──
  var ovbg = document.createElement('div'); ovbg.id = 'ov-bg';
  var sheet = document.createElement('div'); sheet.id = 'ov-sheet';
  sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true');
  sheet.tabIndex = -1;
  sheet.innerHTML = '<button class="ov-close" aria-label="Back to the structure">✕</button>' +
                    '<div class="ov-inner"></div>';
  document.body.appendChild(ovbg); document.body.appendChild(sheet);
  var ovInner = sheet.querySelector('.ov-inner');
  var heldBuilt = null, recWrap = null;
  if (recSec) {
    // the inline reception layer relocates into the overlay — the base
    // view is pure structure now (the one-page shape); the section's
    // markup (and its file presence for the reachability scan) is kept.
    recWrap = document.createElement('div'); recWrap.id = 'ov-reception';
    recWrap.style.display = 'none';
    recWrap.appendChild(recSec);
    ovInner.appendChild(recWrap);
  }
  function zoneTitle(sec) {
    var h = sec.querySelector('h2, .zone-h, h3');
    return h ? (h.childNodes[0] && h.childNodes[0].textContent || h.textContent).trim() : sec.id;
  }
  function buildHeld() {
    if (heldBuilt) return heldBuilt;
    heldBuilt = document.createElement('div'); heldBuilt.id = 'ov-held';
    var seen = {};
    var total = 0;
    var frag = '';
    document.querySelectorAll('section[id]').forEach(function (sec) {
      if (/-reception$/.test(sec.id)) return;
      var zid = sec.id.replace(/^zone-/, '');
      var rows = '';
      sec.querySelectorAll('.chip, .su, .tc').forEach(function (el) {
        var nmEl = el.querySelector('.nm') || el.querySelector('.tl') || el;
        var b = B ? B[zid + '||' + norm((nmEl.textContent || '').trim())] : null;
        if (!b || !b.read) return;
        b.read.forEach(function (r) {
          if (seen[r.df]) return;
          seen[r.df] = 1; total++;
          var head = (r.translator || r.work) + (r.year ? ', ' + r.year : '') + dupLabel(r);
          rows += '<a class="rl-ed" href="../' + r.url + '"><b style="font-weight:400">' +
                  esc(r.work) + '</b><span class="rl-em">' + esc(head) +
                  ' · read in the archive ↗</span></a>';
        });
      });
      if (rows) frag += '<div class="ov-zone"><h3>' + esc(zoneTitle(sec)) +
                        ' — held editions</h3>' + rows + '</div>';
    });
    heldBuilt.innerHTML = '<h2>Held in this archive — ' + total +
                          ' edition' + (total === 1 ? '' : 's') + '</h2>' +
                          (frag || '<div class="rl-none">Nothing from this map is readable here yet.</div>');
    heldBuilt.style.display = 'none';
    ovInner.appendChild(heldBuilt);
    // Task 39 — one held surface: reception rides the same sheet as a
    // final group ("held here, not yet placed in the structure")
    if (recWrap) {
      var recN = recWrap.querySelectorAll('.tc').length;
      var rh = document.createElement('h3');
      rh.className = 'ov-rec-h';
      rh.textContent = 'Reception — held here, not yet placed in the structure · + ' +
                       recN + ' texts in reception';
      recWrap.insertBefore(rh, recWrap.firstChild);
      ovInner.appendChild(recWrap);
    }
    // the header button derives its count from the same pass
    var hb = document.getElementById('held-btn');
    if (hb) {
      // Task 124b item 6 — say which population. This counts EDITIONS
      // reachable from chips on THIS MAP; the line below it counts TEXTS
      // readable anywhere in the archive, and the two differ by more than
      // their units. Both were true and neither said which it was.
      hb.textContent = 'Browse the ' + total + ' held editions on this map →';
      // 41b: a genuinely empty overlay (no placed editions, no
      // reception) hides its one opener rather than advertise zero
      if (total === 0 && !recWrap) hb.style.display = 'none';
    }
    return heldBuilt;
  }
  function openOverlay() {
    _ready.then(function () {
      buildHeld();
      if (heldBuilt) heldBuilt.style.display = '';
      if (recWrap) recWrap.style.display = '';
      if (recSec) recSec.style.display = '';
      document.body.classList.add('ov-open');
      sheet.focus();
    });
  }
  function closeOverlay() {
    document.body.classList.remove('ov-open');
  }
  ovbg.addEventListener('click', function () { hideSheet(); });
  sheet.querySelector('.ov-close').addEventListener('click', function () { hideSheet(); });
  // the mast button — the room's "Browse the N held editions" opener,
  // carried over; same overlay, two openers
  var mast = document.querySelector('.mast');
  if (mast) {
    var hb = document.createElement('button');
    hb.type = 'button'; hb.id = 'held-btn';
    hb.textContent = 'Browse the held editions →';
    hb.addEventListener('click', function () {
      toggleSheet();
    });
    mast.appendChild(hb);
    _ready.then(function () { buildHeld(); });
  }
  // ── Task 38: one geometry, two derivations — the mandala recounts
  // from bindings in the base view; rights restores the compiled
  // g/a/r. Same paths, new fills; aria recounts per mode.
  var HCOLOR = { held: '#7a5c3a', possible: '#c9ab7a', none: '#ddd6c8', restricted: 'url(#rl-stripes)' };
  function pathAngles(p) {
    var nums = (p.getAttribute('d') || '').split(/[^0-9.eE-]+/).filter(Boolean).map(Number);
    if (nums.length < 4) return null;
    var x1 = nums[2], y1 = nums[3], x2 = nums[nums.length - 2], y2 = nums[nums.length - 1];
    var a1 = Math.atan2(y1, x1), a2 = Math.atan2(y2, x2);
    var span = a2 - a1;
    while (span <= 0) span += Math.PI * 2;
    return { start: a1, span: span };
  }
  function updateMandala() {
    var svg = document.getElementById('mandala');
    if (!svg) return;
    if (!svg.dataset.rSaved) {
      svg.dataset.rAria = svg.getAttribute('aria-label') || '';
      svg.querySelectorAll('path.seg').forEach(function (p) { p.dataset.rFill = p.getAttribute('fill'); });
      svg.querySelectorAll('g.zone').forEach(function (z) { z.dataset.rZaria = z.getAttribute('aria-label') || ''; });
      if (!svg.querySelector('#rl-stripes')) {
        var NS = 'http://www.w3.org/2000/svg';
        var defs = document.createElementNS(NS, 'defs');
        var pat = document.createElementNS(NS, 'pattern');
        pat.setAttribute('id', 'rl-stripes'); pat.setAttribute('width', '4'); pat.setAttribute('height', '4');
        pat.setAttribute('patternUnits', 'userSpaceOnUse'); pat.setAttribute('patternTransform', 'rotate(45)');
        var r1 = document.createElementNS(NS, 'rect');
        r1.setAttribute('width', '4'); r1.setAttribute('height', '4'); r1.setAttribute('fill', '#eee9e0');
        var r2 = document.createElementNS(NS, 'rect');
        r2.setAttribute('width', '2'); r2.setAttribute('height', '4'); r2.setAttribute('fill', '#a09080');
        pat.appendChild(r1); pat.appendChild(r2); defs.appendChild(pat); svg.insertBefore(defs, svg.firstChild);
      }
      svg.dataset.rSaved = '1';
    }
    var zones = svg.querySelectorAll('g.zone');
    var secs = document.querySelectorAll('section[id^="zone-"]');
    if (!B) {   // Task 119: the bindings derivation is the only one now
      svg.setAttribute('aria-label', svg.dataset.rAria);
      svg.querySelectorAll('path.seg').forEach(function (p) { p.setAttribute('fill', p.dataset.rFill); });
      zones.forEach(function (z) { z.setAttribute('aria-label', z.dataset.rZaria); });
      return;
    }
    svg.setAttribute('aria-label',
      'Concentric-ring diagram of the Hindu textual tradition, coloured by what the archive holds');
    zones.forEach(function (z, zi) {
      var sec = secs[zi];
      var zid = sec ? sec.id.replace('zone-', '') : null;
      var m = { held: 0, possible: 0, none: 0, restricted: 0 };
      if (zid) Object.keys(B).forEach(function (k) {
        if (k.split('||')[0] !== zid) return;
        var s = B[k].state;
        if (s === 'held' || s === 'held-several') m.held++;
        else if (s === 'possible') m.possible++;
        else if (s === 'restricted') m.restricted++;
        else m.none++;
      });
      var total = m.held + m.possible + m.none + m.restricted;
      var segs = [];
      z.querySelectorAll('path.seg').forEach(function (p) {
        var a = pathAngles(p); if (a) segs.push({ p: p, a: a });
      });
      if (!total || !segs.length) return;
      segs.sort(function (x, y) { return x.a.start - y.a.start; });
      var totalSpan = 0; segs.forEach(function (s) { totalSpan += s.a.span; });
      var bands = [], cum = 0;
      ['held', 'possible', 'none', 'restricted'].forEach(function (st) {
        cum += m[st] / total; bands.push({ st: st, upto: cum });
      });
      var walked = 0;
      segs.forEach(function (s) {
        var mid = (walked + s.a.span / 2) / totalSpan; walked += s.a.span;
        var st = 'restricted';
        for (var i = 0; i < bands.length; i++) { if (mid <= bands[i].upto + 1e-9) { st = bands[i].st; break; } }
        s.p.setAttribute('fill', HCOLOR[st]);
      });
      var name = (z.dataset.rZaria || '').split(':')[0];
      z.setAttribute('aria-label', name + ': ' + m.held + ' readable here, ' + m.possible +
        ' possible, ' + m.none + ' none' + (m.restricted ? ', ' + m.restricted + ' restricted' : ''));
    });
  }
  // Task 119 — THE TASK 38b LEDE-SWAP MACHINERY IS RETIRED. It existed
  // to say one thing in the base view and another in Rights: it split
  // the mast lede at its colour sentence, wrapped each phrasing in
  // .b-only / .r-only, and did the same for the footer sentence and the
  // zone-key "· N PD" counts. With one view there is no second phrasing
  // to swap to, so the machinery goes and the twenty colour sentences
  // are retired from the rooms' own markup rather than re-scoped here.
  //
  // Two consequences worth stating, because neither is a deletion:
  //  · the zone-key "· N PD" count stops being conditional and is
  //    simply visible. It is an aggregate per zone — the .statband
  //    argument exactly — so it survives while the .keyrow .mini BARS
  //    (which restate the marks) retire.
  //  · indigenous' clause "with the traditions that should not be
  //    mapped shown as such" is NOT a colour gloss but the room's
  //    ethical position, and is kept by the sentence retirement.

  // 40a — the sub-tradition pills were NEVER wired when the frames
  // were ported (the artifact's tab JS was not captured; the views
  // shipped stacked). Wire them: one view at a time, first pill =
  // the default, aria-pressed carries the state. Works in both
  // lenses (the rights capture handler ignores [data-view] buttons).
  var viewPills = document.querySelectorAll('[data-view]');
  if (viewPills.length) {
    var showView = function (k) {
      document.querySelectorAll('section.view').forEach(function (v) {
        v.hidden = (v.id !== 'view-' + k);
      });
      viewPills.forEach(function (b2) {
        b2.setAttribute('aria-pressed', b2.getAttribute('data-view') === k ? 'true' : 'false');
      });
    };
    viewPills.forEach(function (b2) {
      b2.addEventListener('click', function () { showView(b2.getAttribute('data-view')); });
    });
    showView(viewPills[0].getAttribute('data-view'));
  }

  // 47c — the mandala earns its place: persistent numeral labels at
  // each zone (matching the zone-key card numerals), click-to-jump
  // via window.scrollTo (never scrollIntoView on the shared surface),
  // and hover sync with the zone-key cards.
  function mandalaNav() {
    var svg = document.getElementById('mandala');
    if (!svg || svg.dataset.navved) return;
    svg.dataset.navved = '1';
    var zones = svg.querySelectorAll('g.zone');
    var secs = document.querySelectorAll('section[id^="zone-"]');
    var keyrows = document.querySelectorAll('.keyrow');
    var LBL = ['◉', '1', '2', '3', '4', '5', 'A', 'B', 'C', 'D'];
    var NS = 'http://www.w3.org/2000/svg';
    zones.forEach(function (z, zi) {
      var pts = [];
      z.querySelectorAll('path.seg').forEach(function (pp) {
        var a = pathAngles(pp);
        var nums = (pp.getAttribute('d') || '').split(/[^0-9.eE-]+/).filter(Boolean).map(Number);
        if (a) pts.push({ mid: a.start + a.span / 2, r: nums.length > 4 ? nums[4] : 40 });
      });
      if (pts.length && LBL[zi]) {
        var mid = pts[0].mid, r = 0;
        pts.forEach(function (q) { if (q.r > r) r = q.r; });
        var t = document.createElementNS(NS, 'text');
        t.setAttribute('x', (Math.cos(mid) * r * 0.72).toFixed(1));
        t.setAttribute('y', (Math.sin(mid) * r * 0.72).toFixed(1));
        t.setAttribute('class', 'mz-lbl');
        t.setAttribute('text-anchor', 'middle');
        t.setAttribute('dominant-baseline', 'central');
        t.textContent = LBL[zi];
        z.appendChild(t);
      }
      z.style.cursor = 'pointer';
      function jump() {
        var sec = secs[zi];
        if (!sec) return;
        var top = sec.getBoundingClientRect().top + window.pageYOffset - 70;
        window.scrollTo({ top: top, behavior: 'smooth' });
        var hh = sec.querySelector('h2, .zone-h');
        if (hh) {
          if (!hh.hasAttribute('tabindex')) hh.setAttribute('tabindex', '-1');
          hh.focus({ preventScroll: true });
        }
      }
      z.addEventListener('click', jump);
      z.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); jump(); }
      });
      var kr = keyrows[zi];
      if (kr) {
        z.addEventListener('mouseenter', function () { kr.classList.add('mz-hl'); });
        z.addEventListener('mouseleave', function () { kr.classList.remove('mz-hl'); });
        kr.addEventListener('mouseenter', function () { z.classList.add('mz-hl'); });
        kr.addEventListener('mouseleave', function () { z.classList.remove('mz-hl'); });
      }
    });
  }
  _ready.then(function () { updateMandala(); mandalaNav(); });

  // Task 119e — THE STATBAND RE-DERIVES FROM THE FOUR MARKS.
  // Task 119 item 4 kept it because it states the aggregate the marks
  // cannot; after the merge it was still counting the OLD g/a/r
  // partition, which cuts the corpus differently — jain proves it:
  // green 5 = held 2 + PD 3, while amber 6 + red 7 = no-PD 13. An
  // aggregate of a partition the page no longer shows states nothing
  // the page means. The tiles now count the binder's m-* states, in the
  // legend's order and vocabulary, derived from bindings, never typed.
  //
  // GATED ON WHAT THE BAND SAYS, NOT ON WHICH ROOM IT IS. Buddhist's
  // statband is not a rights figure at all but a structural one —
  // "5 Vinaya · 34 Dīgha · 152 Majjhima · 56 Saṃyutta …" — and
  // re-deriving it would have destroyed a real count. A band that does
  // not speak green/amber/red is left exactly as it stands.
  // the four-mark counts, one derivation shared by the statband and the
  // totalbar — the two names the same aggregate goes by
  function markCounts() {
    var c = { held: 0, possible: 0, none: 0, restricted: 0, unmapped: 0 }, total = 0;
    Object.keys(B).forEach(function (k) {
      var s = B[k].state; total++;
      if (s === 'held' || s === 'held-several') c.held++;
      else if (s === 'possible') c.possible++;
      else if (s === 'restricted') c.restricted++;
      else if (s === 'unmapped') c.unmapped++;
      else c.none++;
    });
    c.total = total;
    return c;
  }

  // Task 121 item 2 — HINDU'S #totalbar RE-DERIVES, by the same gate.
  // It is the statband figure under another name: hindu is the one room
  // with no statband, and its proportional bar was still reading
  // "162 public-domain · 148 copyright · 22 no English" — the partition
  // the page stopped showing. Same rule as the band: act only if the
  // element speaks the OLD vocabulary, so a bar that has been re-authored
  // (or any future room's) is left alone by construction.
  function restateTotalbar() {
    var bar = document.querySelector('#totalbar');
    if (!bar || !B) return;
    var txt = (bar.textContent || '').toLowerCase();
    if (!/public-domain|copyright|no english/.test(txt)) return;
    var c = markCounts();
    if (!c.total) return;
    // the mark palette, as FILLS — a proportional bar cannot be hollow,
    // so 'PD but unheld' takes the light green of the same family rather
    // than a fourth hue, keeping the legend's vocabulary intact
    var segs = [
      { n: c.held, cls: 'tg', bg: '#2E7D32', dark: '#7fae86', label: 'held' },
      { n: c.possible, cls: 'tp', bg: '#8cbf92', dark: '#5f8f68', label: 'PD' },
      { n: c.none, cls: 'ta', bg: '#B7791F', dark: '#d9a05b', label: 'no PD' },
      { n: c.restricted, cls: 'tr', bg: '#C0392B', dark: '#d97b6c', label: 'restricted' }
    ].filter(function (s) { return s.n > 0; });
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    bar.innerHTML = segs.map(function (s) {
      var pct = (s.n / c.total * 100);
      return '<span class="' + s.cls + '" style="width:' + pct + '%;background:' +
             (dark ? s.dark : s.bg) + '" title="' + s.n + ' ' + esc(s.label) + '">' +
             s.n + ' ' + esc(s.label) + '</span>';
    }).join('');
    bar.setAttribute('aria-label',
      segs.map(function (s) { return s.n + ' ' + s.label; }).join(', '));
  }
  _ready.then(restateTotalbar);
  // the bar carries literal fills, so it must be repainted when the
  // reader flips the lamp — the statband uses tokens and does not
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('#arch-dark, #themeBtn'))
      setTimeout(restateTotalbar, 0);
  });

  // ── Task 123 item 3 — the bands retire, EXCEPT a structural one ──
  // The gate is the one from 119e, reused rather than restated: read
  // what the band SAYS. A band whose tiles are rights states is the
  // aggregate the derived count line already carries in a sentence, and
  // it goes. A band whose tiles are structural divisions ("5 Vinaya ·
  // 34 Dīgha · 152 Majjhima …") states a fact nothing else on the page
  // states, and it stays — marked, so the stylesheet can show it.
  // The retirement is done in JS with an INLINE !important rather than
  // by a stylesheet rule. A class rule has to win a cascade it does not
  // control — the rooms' own sheets are stamped after this block and
  // have beaten it before — whereas an inline important declaration is
  // beaten by nothing. It also lets the structural exception be decided
  // by reading the band, which a stylesheet cannot do.
  function keepStructuralBands() {
    var RIGHTS = ['texts', 'held', 'pd', 'no pd', 'restricted',
                  'green', 'amber', 'red'];
    document.querySelectorAll('.statband').forEach(function (band) {
      var labels = [].map.call(band.querySelectorAll('.stat span'), function (s) {
        return (s.textContent || '').trim().toLowerCase();
      });
      // structural means NO rights word appears — not merely "some
      // label is unfamiliar". Buddhist carries a mixed band
      // ("texts · PD · © · divisions") that the looser test called
      // structural and would have kept: a rights aggregate wearing one
      // structural label is still the aggregate the count line states.
      var structural = labels.length && !labels.some(function (l) {
        return RIGHTS.indexOf(l) >= 0 || l === '©' || l.indexOf('pd') >= 0;
      });
      // Task 124b item 5 — decide the CLASS; the stylesheet does the
      // showing. No inline style, so nothing here has to win a race with
      // the cascade, and a band wrongly marked structural in markup is
      // un-marked by this derivation rather than merely out-specified.
      band.classList.toggle('structural', !!structural);
    });
    // Task 123b item 1/2 — the per-canon gap line retires with the
    // bands. Task 115 seated it beside the greenline, which is gone,
    // and the ZONE note now carries that statement one level up where
    // the fold is. Leaving it would state the same fact twice.
    // the six selectors this used to hide with inline styles are hidden
    // by the stylesheet now (Task 124b item 5) — at first paint, with no
    // fetch in front of them.
  }

  // ── Task 123 item 4 — the TOC navigates ──
  // Its links carried a data-j zone id and NO handler: they had never
  // navigated. Now they scroll to the zone, and open it first if the
  // reader had folded it (item 5), so a table of contents cannot send
  // someone to a heading with nothing under it.
  function wireToc() {
    document.querySelectorAll('nav.toc a[data-j]').forEach(function (a) {
      if (a.dataset.t123) return;
      a.dataset.t123 = '1';
      a.setAttribute('role', 'link');
      a.setAttribute('tabindex', '0');
      var go = function (e) {
        e.preventDefault();
        var id = a.getAttribute('data-j');
        var sec = document.getElementById(id) || document.getElementById('zone-' + id);
        if (!sec) return;
        if (sec.classList.contains('zone-shut')) setZone(sec, true);
        sec.scrollIntoView({ block: 'start', behavior: 'smooth' });
      };
      a.addEventListener('click', go);
      a.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') go(e);
      });
    });
  }

  // ── Task 123 item 5 — COLLAPSE MOVES UP ONE LEVEL ──
  // The zone folds; its families do not. This reverses part of Tasks
  // 98/102/115 deliberately, so Task 115's derivation moves UP with the
  // behaviour rather than being deleted: DERIVE THE DEFAULT, NEVER THE
  // CURRENT VALUE. A zone with no visible content starts closed and
  // says why; a populated zone starts open; after that the zone belongs
  // to the reader and only emptiness is re-asserted.
  // Task 123b — WHAT COUNTS AS A ZONE, stated once.
  // A canon is a VIEW, not the nearest section[id] — Task 115 learned
  // this when `closest('section[id]')` landed on the basket and wrote
  // eight canon lines instead of one, and I walked into the same hole
  // from the other side: `section.view` (view-chinese, view-tibetan)
  // matched the zone test, so the canon view grew its own fold and its
  // own note ON TOP of the baskets inside it — a zone within a zone,
  // and the statement said twice.
  function isZone(sec) {
    return !/-reception$/.test(sec.id)
        && !sec.classList.contains('view')
        && !!sec.querySelector('h2, .zone-h');
  }
  function zoneBody(sec) {
    return [].filter.call(sec.children, function (c) {
      return !/^(H2)$/.test(c.tagName) && !c.classList.contains('zone-h')
             && !c.classList.contains('zone-note');
    });
  }
  function zoneHasContent(sec) {
    return !!sec.querySelector('.tc, .chip, .su');
  }
  // Task 127 — THE PILL RETIRES FOR A CORNER ARROW.
  //
  // Task 125 item 3 ruled the per-zone FOLD pill retires and the zone's
  // own heading becomes its control. What shipped was a pill under every
  // zone title reading FOLD / UNFOLD: the pill did not retire, it moved.
  // Ruled now: one disclosure arrow in the zone box's upper-left corner,
  // and no control beneath the title at all. The arrow's DIRECTION states
  // the state — ▾ open, ▸ shut — so the control says what it did without
  // a word of label.
  function setZone(sec, open) {
    sec.classList.toggle('zone-shut', !open);
    var arrow = sec.querySelector('.zone-arrow');
    if (arrow) {
      arrow.textContent = open ? '▾' : '▸';
      arrow.setAttribute('aria-expanded', open ? 'true' : 'false');
      arrow.setAttribute('aria-label', (open ? 'Fold ' : 'Unfold ') + zoneName(sec));
      arrow.title = (open ? 'Fold ' : 'Unfold ') + zoneName(sec);
    }
  }
  function zoneName(sec) {
    var h = sec.querySelector('h2, .zone-h');
    if (!h) return 'this section';
    var t = '';
    for (var i = 0; i < h.childNodes.length; i++) {
      if (h.childNodes[i].nodeType === 3) t += h.childNodes[i].textContent;
    }
    return (t || h.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  }
  function setupZones() {
    document.querySelectorAll('section[id]').forEach(function (sec) {
      if (!isZone(sec)) return;
      var head = sec.querySelector('h2, .zone-h');
      // Task 124b item 1 — the family loop is gone. Forcing `open` and
      // stamping `fam-flat` here was half of the fight; CSS keyed on
      // `details.fam` now decides what a division shows, on its own.
      // Task 124b item 2 — DERIVE THE DEFAULT ONCE, THEN IT IS THE
      // READER'S — empty or not. The old early-return said exactly that
      // in a comment and then re-closed every contentless zone one line
      // below it, on every run: UNFOLD opened the zone, 125px → 605px,
      // and ~700ms later it snapped shut on its own. A control that
      // visibly does the thing and undoes it is worse than an inert one.
      if (sec.dataset.z123) return;
      sec.dataset.z123 = '1';
      // Task 127 — any pill a previous pass left under the title goes,
      // wherever it was put. Removed by ROLE, not by position, so a
      // control that moved again is still caught.
      [].forEach.call(sec.querySelectorAll('.zone-toggle'), function (old) {
        old.parentNode && old.parentNode.removeChild(old);
      });
      if (!sec.querySelector('.zone-arrow')) {
        var arrow = document.createElement('button');
        arrow.type = 'button';
        arrow.className = 'zone-arrow';
        arrow.addEventListener('click', function (e) {
          e.stopPropagation();
          setZone(sec, sec.classList.contains('zone-shut'));
        });
        // the arrow belongs to the BOX, not the heading — it is placed
        // first so it sits in the corner ahead of everything the zone
        // draws, and CSS pins it there.
        sec.insertBefore(arrow, sec.firstChild);
      }
      // "may also fold on click if that is free" — it is: the heading
      // carries no control of its own now, so the whole line is spare.
      // The arrow stays the visible and ruled control; this is a
      // convenience on top of it, and it must not swallow a click on a
      // link or a chip inside the heading.
      if (head && !head.dataset.z127) {
        head.dataset.z127 = '1';
        head.style.cursor = 'pointer';
        head.addEventListener('click', function (e) {
          if (e.target.closest('a, button, summary, input, select')) return;
          setZone(sec, sec.classList.contains('zone-shut'));
        });
      }
      var populated = zoneHasContent(sec);
      if (!populated && !sec.querySelector('.zone-note')) {
        // Task 123b item 2 — the zone's note is the ONE statement, and
        // it says what the canon actually is. The two cases are
        // DERIVABLE, never listed by room name:
        //   · the zone holds divisions but no texts — it is indexed
        //     from a catalogue and the per-text entries are not held.
        //     That is the Chinese and Tibetan case, and it takes Task
        //     115's own wording, moved up to the fold.
        //   · the zone holds nothing at all — the generic line.
        var catalogued = !!sec.querySelector('details.fam');
        var note = document.createElement('p');
        note.className = 'zone-note';
        note.textContent = catalogued
          ? 'Indexed from the catalogue — no per-text entries held yet.'
          : 'Nothing indexed in this zone yet.';
        head.parentNode.insertBefore(note, head.nextSibling);
      }
      setZone(sec, populated);
    });
  }
  // "Collapse all" folds ZONES now. The room's own Task-98 handler
  // folds `details.fam` and would fight this one, so the button is
  // CLONED first: cloneNode drops every listener bound to the original,
  // which is the cleanest way to retire a handler whose source lives in
  // a file this block does not own.
  // Task 124b item 4 — ONE CONTROL PER VIEW, AND ITS REACH STOPS THERE.
  // `querySelector('.toc-all')` singular was the whole bug. Buddhist
  // carries a nav.toc per canon and only Pāli's markup had a button, so
  // the Chinese and Tibetan views had no control at all — six and two
  // shut zones and no way to open them — while the one button that did
  // exist reached across views: pressed while the reader was in Chinese,
  // it folded Pāli's eight zones, out of sight. Every nav.toc gets a
  // control, and each acts only on the view that holds it.
  function rewireCollapseAll() {
    document.querySelectorAll('nav.toc').forEach(function (nav) {
      var scope = nav.closest('section.view') || document;
      var old = nav.querySelector(':scope > .toc-all');
      var btn;
      if (old) {
        if (old.dataset.t123) return;
        btn = old.cloneNode(true);
        old.parentNode.replaceChild(btn, old);
      } else {
        btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'toc-all';
        nav.insertBefore(btn, nav.firstChild);
      }
      btn.dataset.t123 = '1';
      function zones() {
        return [].filter.call(scope.querySelectorAll('section[id]'), isZone);
      }
      function sync() {
        var anyOpen = zones().some(function (z) { return !z.classList.contains('zone-shut'); });
        btn.textContent = anyOpen ? 'Collapse all' : 'Expand all';
      }
      btn.addEventListener('click', function () {
        var all = zones();
        var anyOpen = all.some(function (z) { return !z.classList.contains('zone-shut'); });
        // Task 124b item 2 — "Expand all" opens an EMPTY zone too. The old
        // rule skipped them, which made this control inert in exactly the
        // two views where every zone is empty. The default is derived
        // once; past that the zone is the reader's, empty or not, and the
        // reader has just asked for it open.
        all.forEach(function (z) { setZone(z, !anyOpen); });
        sync();
      });
      sync();
    });
  }
  // Task 124b item 1 — THE LOOP DIES AT ITS CAUSE.
  // Task 123b re-asserted family openness on every mutation, from an
  // observer watching ['open','class'] — the attributes its own callback
  // wrote. Task 115's derivation re-closed the same empty divisions from
  // the other side. Each woke the other: 3,212 mutations/sec on buddhist,
  // idle, forever; 0/sec at the commit before. Stating the content in CSS
  // fixed what a reader SAW and left the fight burning underneath it.
  // So neither rule survives. The fold is the ZONE (Task 123 item 5), and
  // a division's body is shown by ONE rule — `details.fam > *:not(summary)`
  // in CSS, keyed on a class that is in the static markup. Nothing writes
  // `open` on a family any more, so there is nothing left to race over,
  // and the division renders correctly with JS switched off entirely.
  // THE RULE THIS LEAVES BEHIND: an observer must never watch what its
  // own callback writes. Nothing here observes at all now — the chips are
  // static markup, so one pass after _ready is the whole job.
  _ready.then(function () {
    keepStructuralBands(); setupZones(); wireToc(); rewireCollapseAll();
    flattenFamilies();
  });
  // item 7 — the families' keyboard collapse retires with the mouse one.
  // pointer-events:none stopped the pointer and left <summary> in the tab
  // order at tabIndex 0, still toggling on Enter/Space: 25 dead stops per
  // room announcing an expanded/collapsed state that the loop above made
  // flap. One pass, idempotent, writing an attribute nothing observes.
  function flattenFamilies() {
    document.querySelectorAll('details.fam > summary').forEach(function (s) {
      s.setAttribute('tabindex', '-1');
      s.removeAttribute('role');
      s.setAttribute('aria-hidden', 'true');
    });
  }

  function restatBand() {
    var band = document.querySelector('.statband');
    if (!band || !B) return;
    var labels = [].map.call(band.querySelectorAll('.stat span'), function (s) {
      return (s.textContent || '').trim().toLowerCase();
    });
    var isRights = ['green', 'amber', 'red'].some(function (w) {
      return labels.indexOf(w) >= 0;
    });
    if (!isRights) return;
    var c = markCounts(), total = c.total;
    var rows = [[total, 'texts'], [c.held, 'held'], [c.possible, 'PD'],
                [c.none, 'no PD'], [c.restricted, 'restricted']];
    // the fifth state is named only where it exists — indigenous alone
    if (c.unmapped) rows.push([c.unmapped, 'not mapped']);
    band.innerHTML = rows.map(function (r) {
      return '<div class="stat"><b>' + r[0] + '</b><span>' + esc(r[1]) + '</span></div>';
    }).join('');
  }
  _ready.then(restatBand);

  _ready.then(function () { if (typeof updateMandala === 'function') updateMandala(); });

  // the panel
  var bg = document.createElement('div'); bg.id = 'rl-bg';
  var panel = document.createElement('div'); panel.id = 'rl-panel';
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true');
  panel.tabIndex = -1;
  document.body.appendChild(bg); document.body.appendChild(panel);
  var opener = null;
  function close() {
    document.body.classList.remove('rl-open');
    if (opener) { try { opener.focus(); } catch (e) {} opener = null; }
  }
  bg.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (document.body.classList.contains('ov-open')) hideSheet();
    else close();
  });
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  var RIGHTS = {
    g: 'Green \u2014 a complete public-domain or openly-reusable English translation exists.',
    a: 'Amber \u2014 an English translation exists but is copyrighted, partial, restricted, or not publicly redistributable.',
    r: 'Red \u2014 no English translation has been identified.',
    x: 'Unmapped \u2014 an oral or non-textual tradition; there is no scripture to hold.'
  };
  function edRow(r, chooser) {
    var head = (chooser === 'works')
      ? r.work + (r.translator ? ' \u00b7 ' + r.translator + (r.year ? ', ' + r.year : '') : '')
      : (r.translator || r.work) + (r.year ? ', ' + r.year : '') + dupLabel(r);
    return '<a class="rl-ed" href="../' + r.url + '"><b style="font-weight:400">' + esc(head) + '</b>' +
           '<span class="rl-em">' + esc(r.work) + ' \u00b7 read in the archive \u2197</span></a>';
  }
  function open(el) {
    if (B === null) { _ready.then(function () { open(el); }); return; }
    opener = el;
    var nmEl = el.querySelector('.nm') || el.querySelector('.tl') || el;
    var name = (nmEl.textContent || '').trim();
    if (el.dataset.rlHeading && el.childNodes.length) {
      // headings carry appended zone-bars/count spans — the name is the
      // leading text node only
      name = (el.childNodes[0].textContent || name).trim();
    }
    var sec = el.closest('section[id]');
    var zid = sec ? sec.id.replace(/^zone-/, '') : '';
    var b = B ? B[zid + '||' + norm(name)] : null;
    var p = PROV[nid(name)] || null;
    var pd = (b && b.pd) || ['g', 'a', 'r', 'x'].filter(function (k) { return el.classList.contains(k); })[0] || null;
    var note = el.getAttribute('title') || '';
    var groupH = el.closest('.group') ? el.closest('.group').querySelector('h3') : null;
    var secH = sec ? sec.querySelector('h2, .zone-h') : null;
    var h = '<button class="rl-close" aria-label="Close">\u2715</button>';
    h += '<p class="rl-eyebrow">' + esc((p && p.type) || 'structural node') + '</p>';
    h += '<h3>' + esc((p && p.title) || name) + '</h3>';
    h += '<div class="rl-sec"><div class="rl-lbl">About</div><div class="rl-body">' +
         (p ? esc(p.description) + (p.desc_confidence && p.desc_confidence !== 'reviewed'
              ? ' <span class="rl-conf">\u00b7 derived</span>' : '')
            : 'A fuller reviewed description of this node has not yet been recorded.') + '</div></div>';
    var path = (p && p.path) ? p.path.join(' \u2192 ')
             : [secH ? secH.childNodes[0].textContent.trim() : '', groupH ? groupH.textContent.trim() : '']
               .filter(Boolean).join(' \u2192 ');
    h += '<div class="rl-sec"><div class="rl-lbl">Place in the tradition</div><div class="rl-body">' +
         (esc(path) || '\u2014') + '</div></div>';
    h += '<div class="rl-sec"><div class="rl-lbl">Rights / access (worldwide-PD bar)</div>' +
         (pd ? '<span class="rl-rights ' + pd + '">' + RIGHTS[pd] + '</span>' : '<div class="rl-none">Not classified on this map.</div>') +
         (note ? '<div class="rl-note"><b>Map note:</b> ' + esc(note) + '</div>' : '') + '</div>';
    h += '<div class="rl-sec"><div class="rl-lbl">Read or access online</div>' +
         ((p && p.external && p.external.length)
           ? p.external.map(function (x) {
               return '<a class="rl-ed" href="' + esc(x.url) + '" target="_blank" rel="noopener"><b style="font-weight:400">' +
                      esc(x.edition) + '</b><span class="rl-em">' + esc([x.host, x.access].filter(Boolean).join(' \u00b7 ')) +
                      ' \u00b7 open \u2197</span></a>';
             }).join('')
           : '<div class="rl-none">No exact lawful online source has been recorded yet.</div>') + '</div>';
    // Held in this archive — bindings-derived ONLY (one truth with the holdings lens)
    h += '<div class="rl-sec"><div class="rl-lbl">Held in this archive</div>';
    if (el.dataset.rlHeading) {
      // section/group heading: a derived summary across its chips
      var scope = el.closest('.group') || sec;
      var cs = scope ? scope.querySelectorAll('.chip, .su') : [];
      var m = { read: 0, poss: 0, res: 0, none: 0, n: 0 };
      Array.prototype.forEach.call(cs, function (cel) {
        var cn = cel.querySelector('.nm') || cel.querySelector('.tl') || cel;
        var cb = B ? B[zid + '||' + norm((cn.textContent || '').trim())] : null;
        if (!cb) return;
        m.n++;
        if (cb.read && cb.read.length) m.read++;
        else if (cb.state === 'possible') m.poss++;
        else if (cb.state === 'restricted') m.res++;
        else m.none++;
      });
      h += m.n
        ? '<div class="rl-body">' + m.read + ' of ' + m.n + ' works in this section are readable here' +
          (m.poss ? ' \u00b7 ' + m.poss + ' possible' : '') +
          (m.res ? ' \u00b7 ' + m.res + ' held restricted' : '') + '.</div>'
        : '<div class="rl-none">A structural section \u2014 holdings live on its individual works.</div>';
    } else if (b && b.read && b.read.length) {
      h += '<div class="rl-relh">' + (b.contained_in
            ? 'Available within held complete editions \u2014 ' + esc(b.contained_in)
            : (b.read.length > 1 ? b.read.length + ' held editions' : 'Held edition of this work')) + '</div>';
      h += b.read.map(function (r) { return edRow(r, b.chooser); }).join('');
      (b.restricted_note || []).forEach(function (n) {
        h += '<div class="rl-none">Also held restricted: ' + esc(n.title) + ' (' + esc(n.reason_class) + ').</div>';
      });
    } else if (b && b.state === 'restricted') {
      h += '<div class="rl-none">Held, but restricted (' + esc(b.reason_class || 'rights-or-quality hold') + ') \u2014 not publicly readable.</div>';
    } else if (b && b.state === 'possible') {
      h += '<div class="rl-none">Not held yet \u2014 a public-domain translation exists in the world (amber-possible on this map).</div>';
    } else if (pd === 'x') {
      h += '<div class="rl-none">Nothing to hold \u2014 this node marks an oral tradition.</div>';
    } else {
      h += '<div class="rl-none">No reader-ready edition of this work is held' +
           (pd === 'r' ? ' \u2014 no English translation is known to exist' : '') + '.</div>';
    }
    h += '</div>';
    panel.innerHTML = h;
    panel.querySelector('.rl-close').addEventListener('click', close);
    document.body.classList.add('rl-open');
    panel.focus();
  }
  // Rights mode opens the panel only for chips WITHOUT a door: a chip
  // the binder gave a route keeps its click in BOTH views (Task 103),
  // and that route is now one destination, never a chooser (Task 107).
  // Reception tiles keep their reader links.
  document.addEventListener('click', function (e) {
    if (lens !== 'rights') return;
    var el = e.target.closest('.chip, .su, .tc');
    var isHeading = false;
    if (!el) {
      el = e.target.closest('section[id] h2, .zone-h, .group h3');
      isHeading = !!el;
    }
    if (!el) return;
    var sec = el.closest('section[id]');
    if (sec && /-reception$/.test(sec.id)) return;
    // Task 103 — the chip is always the door. A chip the binder gave a
    // route (role=link for a single witness, role=button for a chooser)
    // keeps its click in BOTH views; the lens may recolour it, never
    // intercept it. The rights panel is reachable from the state dot,
    // which works in both views. Chips with no door are unchanged —
    // their panel is where "why isn't this here, and when" lives.
    var role = el.getAttribute('role');
    var hasDoor = (role === 'link' || role === 'button');
    var onDot = !!(e.target.closest && e.target.closest('.mdot, .dot'));
    if (hasDoor && !onDot) return;
    e.preventDefault(); e.stopPropagation();
    if (isHeading) el.dataset.rlHeading = '1';
    open(el);
  }, true);
  // Task 103 — the state dot opens the rights panel in BOTH views, so
  // the provenance a reader wants is never behind a mode switch.
  document.addEventListener('click', function (e) {
    var dot = e.target.closest && e.target.closest('.mdot, .dot');
    if (!dot) return;
    var el = dot.closest('.chip, .su, .tc');
    if (!el) return;
    var sec = el.closest('section[id]');
    if (sec && /-reception$/.test(sec.id)) return;
    var role = el.getAttribute('role');
    if (role !== 'link' && role !== 'button') return;   // no door: the
    // chip's own click already opens the panel in rights view
    e.preventDefault(); e.stopPropagation();
    open(el);
  }, true);
})();
