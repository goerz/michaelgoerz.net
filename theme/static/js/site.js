// Expand a collapsed section when the URL fragment points to it, e.g.
// categories.html#collapse-tech, and scroll it into view below the sticky
// header. (Safari ignores `scroll-padding-top` for `scrollIntoView`, so the
// offset is computed explicitly.)
(function () {
  function scrollBelowHeader(element) {
    var header = document.querySelector(".site-header");
    var offset = header ? header.getBoundingClientRect().height + 16 : 16;
    var top = element.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top: top });
  }
  function showFragmentTarget() {
    if (!location.hash) return;
    var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target || !target.classList.contains("collapse")) return;
    var scrollToTarget = function () {
      scrollBelowHeader(target.closest(".card") || target);
    };
    if (target.classList.contains("show")) {
      scrollToTarget();
    } else {
      target.addEventListener("shown.bs.collapse", scrollToTarget, { once: true });
      bootstrap.Collapse.getOrCreateInstance(target, { toggle: false }).show();
    }
  }
  document.addEventListener("DOMContentLoaded", showFragmentTarget);
  window.addEventListener("hashchange", showFragmentTarget);
})();
