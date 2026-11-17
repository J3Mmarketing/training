/* J3M 教學資源站 共用互動：深淺色切換、3D 傾斜卡、進場動畫、數字跳動。
   放在 <head> 一般載入（不加 defer），讓深淺色在畫面出現前就套用。 */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;

  /* 深淺色 */
  var saved = null;
  try { saved = localStorage.getItem('j3m-theme'); } catch (e) {}
  if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved);
  window.j3mTheme = function () {
    return root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  };

  /* 3D 傾斜 */
  window.j3mTilt = function (el) {
    if (reduce || !fine || el.__tilt) return;
    el.__tilt = true;
    var max = parseFloat(el.getAttribute('data-tilt') || '7');
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      el.classList.add('is-on');
      el.style.setProperty('--ry', ((x - .5) * max * 2).toFixed(2) + 'deg');
      el.style.setProperty('--rx', ((.5 - y) * max * 2).toFixed(2) + 'deg');
      el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    });
    el.addEventListener('pointerleave', function () {
      el.classList.remove('is-on');
      el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg');
    });
  };

  /* 進場 */
  window.j3mReveal = function (els) {
    if (!('IntersectionObserver' in window) || reduce) { els.forEach(function (el) { el.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  };

  /* 數字跳動 */
  function counters() {
    var nums = document.querySelectorAll('[data-count]');
    if (!('IntersectionObserver' in window) || reduce) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var el = e.target, end = +el.getAttribute('data-count'), t0 = performance.now();
        (function step(t) {
          var p = Math.min(1, (t - t0) / 1400), k = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(end * k);
          if (p < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: .6 });
    Array.prototype.forEach.call(nums, function (el) { el.textContent = '0'; io.observe(el); });
  }

  /* 頁面元素都在之後，統一初始化（動態產生的元素，產生後再呼叫 j3mInit 即可） */
  window.j3mInit = function () {
    Array.prototype.forEach.call(document.querySelectorAll('.tilt'), window.j3mTilt);
    window.j3mReveal(Array.prototype.slice.call(document.querySelectorAll('.reveal:not(.in)')));
  };
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('themeBtn');
    if (btn) btn.addEventListener('click', function () {
      var next = window.j3mTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('j3m-theme', next); } catch (e) {}
      window.dispatchEvent(new CustomEvent('j3m-theme', { detail: next }));
    });
    window.j3mInit();
    counters();
  });
})();
