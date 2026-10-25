(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');
  const meta = document.querySelector('meta[name="theme-color"]');
  const apply = theme => {
    root.setAttribute('data-theme', theme);
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#0b1110' : '#fbf9f9');
    if (toggle) toggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  };
  apply(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
  if (toggle) toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    apply(next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
})();
(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (!button || !nav) return;
  const mobile = window.matchMedia('(max-width: 780px)');
  button.hidden = false;
  document.documentElement.classList.add('navigation-ready');
  const close = () => { button.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { close(); button.focus(); }
  });
  document.addEventListener('click', event => {
    if (!nav.contains(event.target) && !button.contains(event.target)) close();
  });
  mobile.addEventListener('change', close);
})();
