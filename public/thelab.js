// Keep native anchor navigation and move keyboard focus to its destination.
(() => {
  function focusDestination(hash) {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target && target.hasAttribute('tabindex')) {
      target.focus({ preventScroll: true });
    }
  }

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 ||
          event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      focusDestination(link.hash);
    });
  });
  window.addEventListener('hashchange', () => focusDestination(location.hash));
  focusDestination(location.hash);
})();
