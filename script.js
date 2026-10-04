// Progressive enhancements: the page remains usable without JavaScript.
(() => {
  const root = document.documentElement;
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('homepage-theme'); } catch {}
  if (!['light', 'dark'].includes(savedTheme)) savedTheme = null;

  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'theme-toggle';
  document.querySelector('header').append(toggle);

  function applyTheme(theme) {
    root.dataset.theme = theme;
    toggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#202825' : '#deded5';
  }
  applyTheme(savedTheme || (systemTheme.matches ? 'dark' : 'light'));
  toggle.addEventListener('click', () => {
    savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(savedTheme);
    try { localStorage.setItem('homepage-theme', savedTheme); } catch {}
  });
  systemTheme.addEventListener('change', event => {
    if (!savedTheme) applyTheme(event.matches ? 'dark' : 'light');
  });

  // Preserve native anchor navigation while moving keyboard focus to the lab.
  document.querySelector('.lab-link').addEventListener('click', () => {
    document.getElementById('automation-lab').focus({ preventScroll: true });
  });

  const topButton = document.createElement('button');
  topButton.type = 'button';
  topButton.className = 'back-to-top';
  topButton.textContent = 'Back to top ↑';
  topButton.hidden = true;
  document.body.append(topButton);
  const updateTopButton = () => { topButton.hidden = window.scrollY < 300; };
  window.addEventListener('scroll', updateTopButton, { passive: true });
  updateTopButton();
  topButton.addEventListener('click', () => {
    toggle.focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  });
})();
