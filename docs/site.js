/* Quantum Karate — site.js (optional, ~0.6 KB). Scroll reveal only. */
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
    if (el.getBoundingClientRect().top < vh) { el.classList.add('is-in'); return; }
    io.observe(el);
  });
})();
