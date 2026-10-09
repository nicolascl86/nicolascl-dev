// Phase 2 is a local interface preview. Never imply that a request was saved.
(() => {
  const form = document.querySelector('#invitation-request');
  form.addEventListener('submit', event => {
    event.preventDefault();
    form.querySelector('.form-status').textContent = "Requests aren't open yet. Nothing has been sent or saved.";
  });

  const root = document.documentElement;
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const toggle = document.querySelector('.theme-toggle');
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('homepage-theme'); } catch {}
  if (!['light', 'dark'].includes(savedTheme)) savedTheme = null;
  function applyTheme(theme) {
    root.dataset.theme = theme;
    toggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#202825' : '#deded5';
  }
  applyTheme(savedTheme || (systemTheme.matches ? 'dark' : 'light'));
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(savedTheme);
    try { localStorage.setItem('homepage-theme', savedTheme); } catch {}
  });
  systemTheme.addEventListener('change', event => {
    if (!savedTheme) applyTheme(event.matches ? 'dark' : 'light');
  });
  function focusDestination(hash) {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target && target.hasAttribute('tabindex')) target.focus({ preventScroll: true });
  }
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      focusDestination(link.hash);
    });
  });
  window.addEventListener('hashchange', () => focusDestination(location.hash));
  focusDestination(location.hash);
})();
