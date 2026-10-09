/* Quantum Karate — site.js (optional).
   Scroll reveal is skipped when the visitor prefers reduced motion.
   Copy email is separate: the mailto link and the visible address work if this file does not run. */
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

(function () {
  var buttons = document.querySelectorAll('[data-copy-email]');
  if (!buttons.length) return;

  function fallbackCopy(text) {
    var area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.setAttribute('aria-hidden', 'true');
    area.style.position = 'fixed';
    area.style.top = '0';
    area.style.left = '0';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.focus();
    area.select();
    var ok = false;
    try {
      ok = document.execCommand('copy');
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(area);
    if (!ok) throw new Error('copy failed');
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      try {
        fallbackCopy(text);
        resolve();
      } catch (err) {
        reject(err);
      }
    });
  }

  buttons.forEach(function (btn) {
    var status = btn.nextElementSibling;
    if (!status || !status.hasAttribute('data-copy-status')) status = null;
    var timer = 0;
    btn.addEventListener('click', function () {
      var email = btn.getAttribute('data-copy-email') || '';
      copyText(email).then(function () {
        if (!status) return;
        status.textContent = '';
        window.requestAnimationFrame(function () {
          status.textContent = 'Copied';
        });
        window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          status.textContent = '';
        }, 2000);
      }, function () {
        if (status) status.textContent = '';
      });
    });
  });
})();
