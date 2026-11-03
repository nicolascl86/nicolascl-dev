// Privacy-friendly page counts (GoatCounter: no cookies, so no consent banner).
// Only the live domain is counted, never local or Firebase preview builds.
// To change accounts, edit GOATCOUNTER_CODE (the part before .goatcounter.com).
(() => {
  const GOATCOUNTER_CODE = 'nicolascl';
  if (!GOATCOUNTER_CODE || !['nicolascl.dev', 'www.nicolascl.dev'].includes(location.hostname)) return;
  const counter = document.createElement('script');
  counter.async = true;
  counter.dataset.goatcounter = `https://${GOATCOUNTER_CODE}.goatcounter.com/count`;
  counter.src = 'https://gc.zgo.at/count.js';
  document.head.append(counter);
})();
// Shared progressive enhancements for every page.
(() => {
  const root = document.documentElement;
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('homepage-theme'); } catch {}
  if (!['light', 'dark'].includes(savedTheme)) savedTheme = null;
  const header = document.querySelector('header');
  if (!header) return;
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'theme-toggle';
  header.append(toggle);
  function applyTheme(theme) {
    root.dataset.theme = theme;
    toggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) themeColor.content = theme === 'dark' ? '#18161d' : '#f8f7fa';
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
  const topButton = document.createElement('button');
  topButton.type = 'button';
  topButton.className = 'back-to-top';
  topButton.textContent = 'Back to top ↑';
  topButton.hidden = true;
  document.body.append(topButton);
  const updateTopButton = () => { topButton.hidden = window.scrollY < 500; };
  window.addEventListener('scroll', updateTopButton, { passive: true });
  updateTopButton();
  topButton.addEventListener('click', () => {
    toggle.focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  });
})();
