// ÉTHÉRÉE — subtle interactions only
document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.nav');
  const onScroll = () => nav.classList.toggle('solid', window.scrollY > 60);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
      toggle.textContent = links.classList.contains('open') ? '✕' : '☰';
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('open'); toggle.textContent = '☰';
    }));
  }

  // model roster filter (models.html)
  const filterBar = document.querySelector('.filter-bar');
  if (filterBar) {
    const cards = document.querySelectorAll('.roster .model-card');
    filterBar.addEventListener('click', e => {
      const btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      filterBar.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
      const f = btn.dataset.filter;
      cards.forEach(c => {
        c.style.display = (f === 'all' || (c.dataset.cat || '').split(' ').includes(f)) ? '' : 'none';
      });
    });
  }

  // scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
});
