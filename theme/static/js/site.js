// Expand a collapsed section when the URL fragment points to it, e.g.
// categories.html#collapse-tech. The offset for the fixed navbar is handled
// by `scroll-padding-top` in style.css.
(function () {
  function showFragmentTarget() {
    if (!location.hash) return;
    var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target || !target.classList.contains("collapse")) return;
    var scrollToTarget = function () {
      (target.closest(".card") || target).scrollIntoView();
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
