// ASCO v2 — "How ASCO works" pinned scroll story (GSAP ScrollTrigger).
(() => {
  const story = document.querySelector('.story');
  if (!story) return;

  // Stage is authored in a 520x460 coordinate space; scale it to the column.
  const wrap = story.querySelector('.story__stage-wrap');
  const stage = story.querySelector('.st-stage');
  const fit = () => {
    const s = Math.min(1.08, wrap.clientWidth / 520);
    stage.style.transform = `scale(${s})`;
    wrap.style.height = `${460 * s}px`;
  };
  fit();
  window.addEventListener('resize', fit);

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) return; // static finished state stays

  gsap.registerPlugin(ScrollTrigger);
  story.classList.add('story--anim');

  const q = (s) => [...story.querySelectorAll(s)];
  const receipts = q('.st-receipt');
  const rows = q('.st-row');
  const texts = q('.story__text');
  const rail = q('.story__rail li');
  const growth = story.querySelector('.st-growth path');

  // Scene 1 layout: scattered paperwork (x, y, rotation) in stage units.
  const MESSY = [[20, 30, -12], [300, 10, 9], [170, 122, -4], [330, 150, 14], [10, 222, 7], [250, 262, -10], [70, 362, -6], [320, 352, 11]];
  receipts.forEach((r, i) => gsap.set(r, { x: MESSY[i][0], y: MESSY[i][1], rotation: MESSY[i][2] }));

  gsap.set('.st-ledger', { autoAlpha: 0, y: 20 });
  gsap.set(rows, { autoAlpha: 0, x: -12 });
  gsap.set('.st-doc', { autoAlpha: 0, y: 24, scale: 0.96 });
  gsap.set('.st-stamp', { autoAlpha: 0, scale: 1.6, rotation: -24 });
  gsap.set(['.st-kpi', '.st-chart'], { autoAlpha: 0, y: 24 });
  gsap.set('.st-bars i', { scaleY: 0.06 });
  gsap.set(growth, { strokeDasharray: 1, strokeDashoffset: 1, autoAlpha: 0 });
  gsap.set('.st-badge', { autoAlpha: 0, scale: 0.9, y: 6 });
  gsap.set(texts.slice(1), { autoAlpha: 0, y: 24 });

  const tl = gsap.timeline({
    defaults: { ease: 'power3.out' },
    onUpdate: () => setRail(tl.time()),
    scrollTrigger: {
      trigger: story,
      pin: '.story__pin',
      start: 'top top',
      end: '+=460%',
      scrub: 0.8,
      anticipatePin: 1,
    },
  });

  const swap = (from, to, at) => {
    tl.to(texts[from], { autoAlpha: 0, y: -20, duration: 0.35, ease: 'power2.out' }, at);
    tl.to(texts[to], { autoAlpha: 1, y: 0, duration: 0.45 }, `${at}+=0.25`);
  };
  const hold = (d) => tl.to({}, { duration: d });

  // 1 — Before ASCO: messy paperwork + alerts (hold so it reads)
  tl.addLabel('s1', 0);
  hold(0.6);

  // 2 — Organize: each receipt flies into its ledger row
  tl.addLabel('s2');
  swap(0, 1, 's2');
  tl.to('.st-alert', { autoAlpha: 0, y: -10, duration: 0.4 }, 's2');
  tl.to('.st-ledger', { autoAlpha: 1, y: 0, duration: 0.5 }, 's2');
  receipts.forEach((r, i) => {
    // row centre (260, 106 + 40i) minus half the receipt (90, 30)
    tl.to(r, { x: 170, y: 76 + i * 40, rotation: 0, scale: 0.55, autoAlpha: 0, duration: 0.7, ease: 'power2.inOut' }, `s2+=${0.15 + i * 0.07}`);
    tl.to(rows[i], { autoAlpha: 1, x: 0, duration: 0.35 }, `s2+=${0.55 + i * 0.07}`);
  });
  hold(0.6);

  // 3 — Comply: ledger rolls up into a VAT return, FTA stamp lands
  tl.addLabel('s3');
  swap(1, 2, 's3');
  tl.to(rows, { autoAlpha: 0, y: -14, duration: 0.35, stagger: 0.04 }, 's3');
  tl.to('.st-ledger', { autoAlpha: 0, scale: 0.97, duration: 0.4 }, 's3+=0.35');
  tl.to('.st-doc', { autoAlpha: 1, y: 0, scale: 1, duration: 0.5 }, 's3+=0.45');
  tl.from('.st-line', { autoAlpha: 0, x: -10, duration: 0.3, stagger: 0.08 }, 's3+=0.7');
  tl.to('.st-stamp', { autoAlpha: 1, scale: 1, rotation: -12, duration: 0.35, ease: 'power4.out' }, 's3+=1.2');
  hold(0.6);

  // 4 — Report: return tucks away, dashboard builds
  tl.addLabel('s4');
  swap(2, 3, 's4');
  tl.to('.st-doc', { x: -115, y: -110, scale: 0.45, duration: 0.7, ease: 'power2.inOut' }, 's4');
  tl.to('.st-kpi', { autoAlpha: 1, y: 0, duration: 0.45, stagger: 0.12 }, 's4+=0.45');
  tl.to('.st-chart', { autoAlpha: 1, y: 0, duration: 0.45 }, 's4+=0.55');
  tl.to('.st-bars i', { scaleY: 0.72, duration: 0.5, stagger: 0.05 }, 's4+=0.8');
  hold(0.5);

  // 5 — Grow: bars rise, growth line draws, badge
  tl.addLabel('s5');
  swap(3, 4, 's5');
  tl.to('.st-bars i', { scaleY: 1, duration: 0.6, stagger: 0.04, ease: 'power2.inOut' }, 's5');
  tl.set(growth, { autoAlpha: 1 }, 's5+=0.2');
  tl.to(growth, { strokeDashoffset: 0, duration: 0.9, ease: 'power1.inOut' }, 's5+=0.2');
  tl.to('.st-badge', { autoAlpha: 1, scale: 1, y: 0, duration: 0.35 }, 's5+=0.9');
  hold(0.7);

  const marks = ['s1', 's2', 's3', 's4', 's5'].map((l) => tl.labels[l]);
  function setRail(t) {
    let on = 0;
    marks.forEach((m, i) => { if (t >= m - 0.05) on = i; });
    rail.forEach((li, i) => {
      li.classList.toggle('is-on', i === on);
      li.classList.toggle('is-done', i < on);
    });
  }
  setRail(0);

  window.addEventListener('load', () => ScrollTrigger.refresh());
})();
