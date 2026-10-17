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

// Toggle between the light and dark color theme. The inline script in the
// <head> of base.html applies the theme on page load. An explicit choice is
// remembered, unless it matches the system setting, in which case the site
// follows the system setting again.
(function () {
  var systemDark = matchMedia("(prefers-color-scheme: dark)");
  function systemTheme() {
    return systemDark.matches ? "dark" : "light";
  }
  function storedTheme() {
    try { return localStorage.getItem("theme"); } catch (e) { return null; }
  }
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    var label = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
    document.querySelectorAll(".theme-toggle").forEach(function (button) {
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
    });
  }
  function toggleTheme() {
    var theme = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
    try {
      if (theme === systemTheme()) {
        localStorage.removeItem("theme");
      } else {
        localStorage.setItem("theme", theme);
      }
    } catch (e) {}
    applyTheme(theme);
  }
  systemDark.addEventListener("change", function () {
    var theme = storedTheme();
    if (theme !== "light" && theme !== "dark") applyTheme(systemTheme());
  });
  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(document.documentElement.getAttribute("data-bs-theme") || systemTheme());
    document.querySelectorAll(".theme-toggle").forEach(function (button) {
      button.addEventListener("click", toggleTheme);
    });
  });
})();
