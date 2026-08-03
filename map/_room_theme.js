(function () {
  // Task 47d — ONE theme key (da-theme), already applied pre-paint by
  // the head boot; the toggle writes the shared key.
  var KEY = 'da-theme';
  function flip() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
    localStorage.setItem(KEY, dark ? 'light' : 'dark');
    label();
  }
  function label() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('#arch-dark, #themeBtn').forEach(function (b) {
      b.textContent = dark ? '☀︎' : '☾';
    });
  }
  document.querySelectorAll('#arch-dark, #themeBtn').forEach(function (b) {
    b.addEventListener('click', flip);
  });
  label();

  function norm(s) {
    return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
            .replace(/^the\s+/, '').replace(/[^a-z0-9]+/g, '');
  }

  var SLUG = document.body.getAttribute('data-map');
  if (!SLUG) return;
  (window.__bindingsP || (window.__bindingsP = fetch('../maps/' + SLUG + '/bindings.json').then(function (r) { return r.json(); })))
  .then(function (B) {
    var byKey = {};
    B.chips.forEach(function (c) { byKey[c.zone + '||' + norm(c.chip)] = c; });
    document.querySelectorAll('section[id]').forEach(function (sec) {
      var zid = sec.id.replace(/^zone-/, '');
      var states = [];
      sec.querySelectorAll('.chip, .tc, .su').forEach(function (el) {
        var nmEl = el.querySelector('.nm') || el.querySelector('.tl') ||
                   el.querySelector('span:last-child');
        if (!nmEl) return;
        var b = byKey[zid + '||' + norm(nmEl.textContent)];
        if (!b) return;
        states.push(b.state);
        el.classList.add('m-' + b.state.replace('held-several', 'several'));
        if (!el.querySelector('.mdot')) {
          var d = document.createElement('span');
          d.className = 'mdot';
          el.insertBefore(d, el.firstChild);
        }
        if (b.restricted_note) {
          el.title = (el.title ? el.title + ' — ' : '') + b.restricted_note.length +
                     ' related record(s) held restricted (' +
                     b.restricted_note[0].reason_class + ')';
        }
        if (b.contained_in) {
          el.title = (el.title ? el.title + ' — ' : '') + b.contained_in;
        }
        if ((b.state === 'held' || b.state === 'held-several') && b.read && b.read.length) {
          // Task 107 — the chip is the door, and the door has ONE
          // destination. The chooser popover retires: it put a choice
          // between editions one layer BEFORE the contents page offers
          // the same choice better — inside the work's own plate, with
          // "N other editions" (Tasks 82/99). Single-held behaviour is
          // unchanged; it is now the only behaviour, in both views.
          el.style.cursor = 'pointer';
          el.setAttribute('role', 'link');
          el.setAttribute('tabindex', '0');
          el.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
          });
          el.addEventListener('click', function () {
            // Task 108 — the contents page is told WHICH chip sent the
            // reader. It decides two things there: the 'also bound here'
            // group (witnesses this chip binds that are not editions of
            // the landing work) and the arrival line. norm() is the
            // lens's own, so the reader matches it back to the binding.
            location.href = '../' + b.read[0].url +
                            '&chip=' + encodeURIComponent(norm(b.chip));
          });
        }
      });
      if (states.length) {
        var held = 0, poss = 0, none = 0, res = 0;
        states.forEach(function (s) {
          if (s === 'held' || s === 'held-several') held++;
          else if (s === 'possible') poss++;
          else if (s === 'restricted') res++;
          else none++;
        });
        var n = states.length;
        var bar = document.createElement('span');
        bar.className = 'zb';
        bar.innerHTML = '<i class="zb-held" style="width:' + (held * 100 / n) + '%"></i>' +
                        '<i class="zb-poss" style="width:' + (poss * 100 / n) + '%"></i>' +
                        '<i class="zb-none" style="width:' + (none * 100 / n) + '%"></i>' +
                        '<i class="zb-res" style="width:' + (res * 100 / n) + '%"></i>';
        var old = sec.querySelector('.mini');
        var head = sec.querySelector('.zone-h, h2');
        if (old && old.closest('section') === sec) old.replaceWith(bar);
        else if (head) head.appendChild(bar);
      }
    });
    // mast fraction line — derived, never typed
    var held = (B.counts['held'] || 0) + (B.counts['held-several'] || 0);
    // Task 128 item 4 — the "N more acquirable" clause is DELETED, not
    // moved. `poss` went with it rather than being left computed and
    // unused, which is how a retired figure creeps back.
    fetch('../maps/doors.json').then(function (r) { return r.json(); })
    .then(function (D) {
      var door = D.doors.filter(function (d) { return d.tradition === SLUG; })[0];
      var mast = document.querySelector('.mast');
      if (!mast || !door) return;
      var p = document.createElement('p');
      p.id = 'm-fraction';
      // Task 128 item 4 — TWO centred lines under the browse button, and
      // nothing else. Both derived from the binder and the door record,
      // never hand-typed.
      p.innerHTML =
        '<span class="m-l1">' +
          door.sub.replace(/ texts$/, ' texts in the tradition') +
        '</span>' +
        '<span class="m-l2">' + held + ' readable in the archive</span>';
      mast.appendChild(p);
    });
  });
})();
