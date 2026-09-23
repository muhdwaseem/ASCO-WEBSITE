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

  // ===== Business animations =====
  document.querySelectorAll('.svc__chart i').forEach((b, i) => b.style.setProperty('--n', i));
  document.querySelectorAll('.pains li').forEach((li, i) => li.style.setProperty('--i', i));
  document.querySelectorAll('.calendar li').forEach((li, i) => li.style.setProperty('--i', i));
  document.querySelector('.hero__frame')?.classList.add('is-stamped');

  // Live bookkeeping feed in the hero card
  const card = document.querySelector('.float-card--a');
  const ledger = card?.querySelector('.ledger');
  const feed = [
    ['VAT return filed', 'On time · FTA compliant'],
    ['Bank reconciliation', 'All accounts matched'],
    ['Month-end close', 'Management reports delivered'],
    ['Corporate Tax return', 'Prepared & reviewed'],
    ['Books up to date', 'Audit-ready records'],
  ];
  if (ledger && !reduced) {
    let k = 0;
    card.classList.add('is-ticking');
    setInterval(() => {
      ledger.classList.add('is-out');
      card.classList.remove('is-ticking');
      setTimeout(() => {
        k = (k + 1) % feed.length;
        ledger.querySelector('strong').textContent = feed[k][0];
        ledger.querySelector('small').textContent = feed[k][1];
        ledger.classList.remove('is-out');
        void card.offsetWidth;
        card.classList.add('is-ticking');
      }, 320);
    }, 3200);
  }

  // Process timeline fills as you scroll
  const steps = document.querySelector('.steps');
  const stepItems = steps ? [...steps.querySelectorAll('.step')] : [];
  const onSteps = () => {
    if (!steps) return;
    const r = steps.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (innerHeight * 0.8 - r.top) / Math.max(r.height * 0.9, innerHeight * 0.45)));
    steps.style.setProperty('--p', p.toFixed(3));
    stepItems.forEach((st, i) => st.classList.toggle('is-active', p >= i / (stepItems.length - 1) - 0.02));
  };
  let ticking = false;
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { onSteps(); ticking = false; }); } }, { passive: true });
  onSteps();

  // Count-up numbers
  const pains = document.querySelector('.pains');
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

  // Challenges flip to "Solved" once the list is well in view
  if (pains) {
    const po = new IntersectionObserver(([en]) => {
      if (en.isIntersecting) { setTimeout(() => pains.classList.add('is-solved'), reduced ? 0 : 700); po.disconnect(); }
    }, { threshold: 0.6 });
    po.observe(pains);
  }
})();
