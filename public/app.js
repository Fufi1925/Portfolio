(() => {
  const header = document.querySelector('[data-header]');
  const menuButton = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');

  const setHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 24);
  setHeader();
  window.addEventListener('scroll', setHeader, { passive: true });

  menuButton?.addEventListener('click', () => {
    const open = menu?.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(Boolean(open)));
  });

  menu?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('is-open');
      menuButton?.setAttribute('aria-expanded', 'false');
    });
  });

  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-category]')];
  filters.forEach((button) => {
    button.addEventListener('click', () => {
      filters.forEach((item) => item.classList.toggle('is-active', item === button));
      const filter = button.dataset.filter;
      cards.forEach((card) => {
        const categories = card.dataset.category.split(' ');
        card.classList.toggle('is-hidden', filter !== 'all' && !categories.includes(filter));
      });
    });
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px' });
    revealItems.forEach((item) => observer.observe(item));
  }

  document.querySelectorAll('[data-year]').forEach((item) => {
    item.textContent = new Date().getFullYear();
  });
})();
