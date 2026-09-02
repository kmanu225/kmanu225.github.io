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
