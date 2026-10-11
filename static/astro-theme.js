/* Runs before paint; preference is optional when storage is unavailable. */
(function () {
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try { preference = localStorage.getItem('astro-theme') || 'system'; } catch (_) {}
  if (!['system', 'light', 'dark'].includes(preference)) preference = 'system';
  function apply() {
    document.documentElement.dataset.theme = preference === 'system' ? (media.matches ? 'dark' : 'light') : preference;
  }
  apply();
  media.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('astro-theme');
    select.value = preference;
    select.addEventListener('change', () => {
      preference = select.value;
      try { localStorage.setItem('astro-theme', preference); } catch (_) {}
      apply();
    });
  });
})();
