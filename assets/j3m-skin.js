/* J3M 教材頁外觀層：沿用全站的深淺色設定，並讓頂部的切換鈕可以切換。
   放在 <head> 一般載入（不加 defer）。 */
(function () {
  var root = document.documentElement;
  if (root.classList.contains('j3m-dark-only')) return;
  var saved = null;
  try { saved = localStorage.getItem('j3m-theme'); } catch (e) {}
  if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved);
  function current() {
    return root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('.j3m-theme');
    if (!btn) return;
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('j3m-theme', next); } catch (err) {}
  });
})();
