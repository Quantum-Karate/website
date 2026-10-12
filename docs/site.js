/* Quantum Karate — site.js. Scroll reveal, plus a copy-email enhancement. */
(function () {
  document.querySelectorAll("[data-copy-email]").forEach(function (btn) {
    var statusId = btn.getAttribute("data-copy-status");
    var status = statusId ? document.getElementById(statusId) : null;
    var timer = 0;
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var email = btn.getAttribute("data-copy-email") || "";
      var showCopied = function () {
        if (!status) return;
        status.textContent = "Copied";
        window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          status.textContent = "";
        }, 5000);
      };
      // Run during the click so the copy still works if the async clipboard
      // call is denied. A later rejection would be outside the user gesture.
      var area = document.createElement("textarea");
      area.value = email;
      area.setAttribute("readonly", "");
      area.setAttribute("aria-hidden", "true");
      area.tabIndex = -1;
      area.style.position = "fixed";
      area.style.top = "0";
      area.style.left = "-9999px";
      // iOS Safari zooms a focused field under 16px and does not zoom back out.
      area.style.fontSize = "16px";
      document.body.appendChild(area);
      area.focus({ preventScroll: true });
      area.select();
      var copied = false;
      try {
        copied = document.execCommand("copy");
      } catch (err) {
        copied = false;
      }
      document.body.removeChild(area);
      btn.focus({ preventScroll: true });
      if (copied) showCopied();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(email).then(showCopied, function () {});
      }
    });
  });
})();
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
