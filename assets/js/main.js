(() => {
  document.documentElement.classList.remove('no-js');
  const nav = document.getElementById('nav');
  const menu = document.getElementById('mobileMenu');
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 24 || !menu.hidden);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const burger = nav.querySelector('.nav__burger');
  const setMenu = (open) => {
    burger.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    onScroll();
  };
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); burger.focus(); } });
  burger.addEventListener('click', () => setMenu(menu.hidden));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });

  // Tabs (business stages) with arrow-key support
  const tabs = [...document.querySelectorAll('.stages__tabs [role="tab"]')];
  const select = (tab) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    tab.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', (e) => {
      const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      const next = tabs[(i + d + tabs.length) % tabs.length];
      select(next); next.focus();
    });
  });

  // Lead form -> WhatsApp with a prefilled message
  const form = document.getElementById('leadForm');
  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const msg = "Hello ASCO, I'd like to book a free consultation.\nName: " + d.get('name') + "\nCompany: " + (d.get('company') || '-') + "\nService: " + d.get('service');
    window.open('https://wa.me/971508216634?text=' + encodeURIComponent(msg), '_blank', 'noopener');
  });

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Count-up numbers
  const countUp = (el) => {
    const target = parseFloat(el.dataset.count);
    const dec = parseInt(el.dataset.decimals || '0', 10);
    if (reduced) return;
    const t0 = performance.now(), dur = 1600;
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  // Reveal on scroll
  if (!('IntersectionObserver' in window)) {
    document.documentElement.classList.add('no-js');
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      en.target.querySelectorAll?.('[data-count]').forEach(countUp);
      if (en.target.matches('[data-count]')) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });
  document.querySelectorAll('.stats [data-count]').forEach((el) => io.observe(el));
})();
