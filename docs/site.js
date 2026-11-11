/* Quantum Karate — site.js. Scroll reveal. */
(function () {
  var d = document.documentElement;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;
  d.classList.add('js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  var vh = window.innerHeight || d.clientHeight;
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    el.addEventListener('focusin', function () { el.classList.add('is-in'); });
    if (el.getBoundingClientRect().top < vh) { el.classList.add('is-in'); return; }
    io.observe(el);
  });
})();

/* Language disclosure: Escape closes, arrows move, click outside closes. */
(function () {
  var menus = document.querySelectorAll('details.lang-switch');
  if (!menus.length) return;

  function linksOf(details) {
    return Array.prototype.slice.call(details.querySelectorAll('a'));
  }

  menus.forEach(function (details) {
    details.addEventListener('keydown', function (e) {
      var links = linksOf(details);
      var summary = details.querySelector('summary');
      if (e.key === 'Escape') {
        if (!details.open) return;
        details.open = false;
        if (summary) summary.focus();
        e.preventDefault();
        return;
      }
      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Home' && e.key !== 'End') return;
      if (!links.length) return;
      e.preventDefault();
      if (!details.open) details.open = true;
      var current = links.indexOf(document.activeElement);
      var next = 0;
      if (e.key === 'ArrowDown') next = current < 0 ? 0 : (current + 1) % links.length;
      else if (e.key === 'ArrowUp') next = current <= 0 ? links.length - 1 : current - 1;
      else if (e.key === 'Home') next = 0;
      else next = links.length - 1;
      links[next].focus();
    });
  });

  document.addEventListener('pointerdown', function (e) {
    menus.forEach(function (details) {
      if (!details.open) return;
      if (!details.contains(e.target)) details.open = false;
    });
  });
})();
