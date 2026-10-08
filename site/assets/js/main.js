/* ==========================================================================
   Remis à Neuf — interactions
   Vanilla JS, sans dépendance. Chaque bloc est autonome et désactivable.
   ========================================================================== */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- 1. Header : état au scroll -------------------------------------- */
  (function header() {
    var hdr = $('.hdr');
    if (!hdr) return;
    var tick = function () { hdr.classList.toggle('is-solid', window.scrollY > 24); };
    tick();
    window.addEventListener('scroll', tick, { passive: true });
  })();

  /* --- 2. Menu mobile --------------------------------------------------- */
  (function menu() {
    var btn = $('.burger');
    var nav = $('.mnav');
    if (!btn || !nav) return;

    var setOpen = function (open) {
      document.body.classList.toggle('menu-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
      btn.setAttribute('aria-expanded', String(open));
      nav.setAttribute('aria-hidden', String(!open));
    };

    btn.addEventListener('click', function () {
      setOpen(!document.body.classList.contains('menu-open'));
    });
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024) setOpen(false);
    });
    setOpen(false);
  })();

  /* --- 3. Apparition au scroll ------------------------------------------ */
  (function reveal() {
    var items = $$('.rv, .mstep');
    if (!items.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  })();

  /* --- 4. FAQ : accordéon ----------------------------------------------- */
  (function accordion() {
    var items = $$('.acc__i');
    if (!items.length) return;

    items.forEach(function (item) {
      var btn = $('.acc__btn', item);
      var panel = $('.acc__p', item);
      if (!btn || !panel) return;

      btn.addEventListener('click', function () {
        var open = item.classList.contains('is-open');
        // Un seul panneau ouvert à la fois
        items.forEach(function (other) {
          other.classList.remove('is-open');
          var b = $('.acc__btn', other);
          var p = $('.acc__p', other);
          if (b) b.setAttribute('aria-expanded', 'false');
          if (p) p.setAttribute('aria-hidden', 'true');
        });
        if (!open) {
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
          panel.setAttribute('aria-hidden', 'false');
        }
      });
    });
  })();

  /* --- 5. Comparateur avant / après ------------------------------------- */
  (function beforeAfter() {
    $$('.ba').forEach(function (ba) {
      var before = $('.ba__before', ba);
      var handle = $('.ba__handle', ba);
      if (!before || !handle) return;

      var pos = 50;

      var sizeImg = function () {
        ba.style.setProperty('--baw', ba.clientWidth + 'px');
      };
      var apply = function () {
        before.style.width = pos + '%';
        handle.style.left = pos + '%';
        handle.setAttribute('aria-valuenow', Math.round(pos));
      };
      var fromClientX = function (x) {
        var r = ba.getBoundingClientRect();
        pos = Math.min(100, Math.max(0, ((x - r.left) / r.width) * 100));
        apply();
      };

      var dragging = false;
      var down = function (e) {
        dragging = true;
        ba.setPointerCapture && e.pointerId != null && ba.setPointerCapture(e.pointerId);
        fromClientX(e.clientX);
      };
      var move = function (e) { if (dragging) fromClientX(e.clientX); };
      var up = function () { dragging = false; };

      ba.addEventListener('pointerdown', down);
      ba.addEventListener('pointermove', move);
      window.addEventListener('pointerup', up);
      ba.addEventListener('pointercancel', up);

      handle.addEventListener('keydown', function (e) {
        var step = e.shiftKey ? 10 : 2;
        if (e.key === 'ArrowLeft')  { pos = Math.max(0, pos - step); apply(); e.preventDefault(); }
        if (e.key === 'ArrowRight') { pos = Math.min(100, pos + step); apply(); e.preventDefault(); }
        if (e.key === 'Home')       { pos = 0;   apply(); e.preventDefault(); }
        if (e.key === 'End')        { pos = 100; apply(); e.preventDefault(); }
      });

      window.addEventListener('resize', sizeImg);
      sizeImg();
      apply();
    });
  })();

  /* --- 6. Formulaire de devis -------------------------------------------
     Point de branchement unique : remplacer `sendLead` par un POST vers
     un endpoint (Formspree, Brevo, HubSpot, API interne…).
     ---------------------------------------------------------------------- */
  (function quoteForm() {
    var form = $('#form-devis');
    if (!form) return;
    var msg = $('#form-msg', form);
    var submit = $('button[type="submit"]', form);

    var ENDPOINT = form.getAttribute('data-endpoint') || '';

    function say(text, ok) {
      if (!msg) return;
      msg.textContent = text;
      msg.classList.add('show');
      msg.style.borderLeftColor = ok ? '#a88f69' : '#b4493f';
    }

    function sendLead(payload) {
      if (!ENDPOINT) {
        // Aucun endpoint configuré : on journalise la soumission pour recette.
        if (window.console) console.info('[Remis à Neuf] Lead (aucun endpoint configuré) :', payload);
        return Promise.resolve({ ok: true, simulated: true });
      }
      return fetch(ENDPOINT, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: payload instanceof FormData ? payload : JSON.stringify(payload)
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof form.reportValidity === 'function' && !form.reportValidity()) return;

      var data = new FormData(form);
      var plain = {};
      data.forEach(function (v, k) { if (!(v instanceof File)) plain[k] = v; });

      if (submit) { submit.disabled = true; submit.style.opacity = '.6'; }

      sendLead(ENDPOINT ? data : plain)
        .then(function (res) {
          if (res && res.ok === false) throw new Error('HTTP');
          say('Merci, votre demande a bien été prise en compte. Nous revenons vers vous rapidement.', true);
          form.reset();
        })
        .catch(function () {
          say('L’envoi a échoué. Merci de réessayer ou de nous contacter directement.', false);
        })
        .finally(function () {
          if (submit) { submit.disabled = false; submit.style.opacity = ''; }
        });
    });
  })();

  /* --- 7. Divers --------------------------------------------------------- */
  (function misc() {
    var y = $('#year');
    if (y) y.textContent = new Date().getFullYear();
    requestAnimationFrame(function () { document.documentElement.classList.add('is-ready'); });
  })();
})();
