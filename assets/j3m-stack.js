/* J3M 3D 層疊畫卡：卡片從左下往右上斜向疊放，滑過會抽出，拖曳可翻卡，點擊開啟。
   用法（頁面裡）：
     import { mountStack } from '<相對路徑>/assets/j3m-stack.js';
     mountStack([{ kicker, title, desc, foot, color, motif, mark, href, ext, tip: { title, body, go } }, ...]);
   回傳 { focus(i), blur() }，也會掛在 window.J3M3D，讓頁面上的 HTML 卡片連動。 */
import * as THREE from './three.module.min.js';

function rr(g, x, y, w, h, r) {
  g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
}
export function shade(hex, k) {
  const n = parseInt(hex.slice(1), 16), r = n >> 16, gg = n >> 8 & 255, b = n & 255;
  const f = v => Math.max(0, Math.min(255, Math.round(k > 0 ? v + (255 - v) * k : v * (1 + k))));
  return '#' + [f(r), f(gg), f(b)].map(v => v.toString(16).padStart(2, '0')).join('');
}

/* 每個主題一種圖形，讓卡片像一幅海報 */
const MOTIF = [
  (g, W, H) => { for (let i = 0; i < 6; i++) { g.strokeStyle = `rgba(255,255,255,${.06 + i * .02})`; g.lineWidth = 3; g.strokeRect(W * .52 + i * 34, 90 + i * 30, 300, 190); } },
  (g, W, H) => { for (let x = W * .5; x < W; x += 26) { g.fillStyle = 'rgba(255,255,255,.08)'; g.fillRect(x, 0, 10, H); } g.fillStyle = 'rgba(245,184,0,.9)'; g.beginPath(); g.moveTo(W * .72, 200); g.lineTo(W * .72, 380); g.lineTo(W * .72 + 150, 290); g.fill(); },
  (g, W, H) => { for (let y = 40; y < H; y += 28) for (let x = W * .5; x < W; x += 28) { g.fillStyle = `rgba(255,255,255,${(x + y) % 3 ? .14 : .32})`; g.beginPath(); g.arc(x, y, 3, 0, 7); g.fill(); } },
  (g, W, H) => { g.strokeStyle = 'rgba(255,255,255,.2)'; g.lineWidth = 2; const cx = W * .76, cy = 280; for (let i = 0; i < 6; i++) { g.beginPath(); g.moveTo(cx, cy - 150 + i * 10); g.lineTo(cx + 170 - i * 20, cy - 60); g.lineTo(cx + 170 - i * 20, cy + 120); g.lineTo(cx, cy + 210 - i * 10); g.lineTo(cx - 170 + i * 20, cy + 120); g.lineTo(cx - 170 + i * 20, cy - 60); g.closePath(); g.stroke(); } },
  (g, W, H) => { [[.66, 200, 130], [.82, 330, 100]].forEach(([x, y, r], k) => { g.fillStyle = k ? 'rgba(255,255,255,.9)' : 'rgba(255,255,255,.18)'; rr(g, W * x - r, y - r * .7, r * 2, r * 1.4, r * .6); g.fill(); }); },
  (g, W, H) => { const c = ['rgba(255,255,255,.18)', 'rgba(245,184,0,.75)', 'rgba(255,255,255,.3)', 'rgba(0,0,0,.25)']; for (let i = 0; i < 9; i++) { g.fillStyle = c[i % 4]; g.fillRect(W * .55 + i * 44, 140 + (i % 3) * 18, 34, 420 - (i % 3) * 18); } },
  (g, W, H) => { g.strokeStyle = 'rgba(255,255,255,.22)'; g.lineWidth = 3; g.beginPath(); g.moveTo(W * .55, 470); [[.62, 380], [.7, 410], [.78, 290], [.86, 320], [.94, 170]].forEach(([px, py]) => g.lineTo(W * px, py)); g.stroke(); g.fillStyle = 'rgba(245,184,0,.9)'; g.beginPath(); g.arc(W * .94, 170, 12, 0, 7); g.fill(); },
  (g, W, H) => { g.strokeStyle = 'rgba(245,184,0,.7)'; g.lineWidth = 3; [150, 110, 70].forEach((r, k) => { g.beginPath(); g.arc(W * .77, 300, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (.9 - k * .2)); g.stroke(); }); }
];

function wrapLines(g, text, maxW, maxLines) {
  const out = []; let line = '';
  for (const ch of text) {
    if (g.measureText(line + ch).width > maxW) {
      out.push(line); line = ch;
      if (out.length === maxLines) { out[maxLines - 1] = out[maxLines - 1].slice(0, -1) + '…'; return out; }
    } else line += ch;
  }
  if (line) out.push(line);
  return out;
}

function cardTexture(d) {
  const W = 1024, H = 640, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d');
  rr(g, 0, 0, W, H, 26); g.save(); g.clip();
  const bg = g.createLinearGradient(0, 0, W, H);
  bg.addColorStop(0, shade(d.color, .22)); bg.addColorStop(.55, d.color); bg.addColorStop(1, shade(d.color, -.45));
  g.fillStyle = bg; g.fillRect(0, 0, W, H);
  const glow = g.createRadialGradient(W * .78, H * .3, 0, W * .78, H * .3, 420);
  glow.addColorStop(0, 'rgba(255,255,255,.22)'); glow.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = glow; g.fillRect(0, 0, W, H);
  MOTIF[(d.motif || 0) % MOTIF.length](g, W, H);
  if (d.mark) { g.fillStyle = 'rgba(255,255,255,.08)'; g.font = '700 190px "JetBrains Mono", monospace'; g.textAlign = 'right'; g.fillText(d.mark, W - 40, H - 40); g.textAlign = 'left'; }
  g.fillStyle = '#F5B800'; g.font = '700 34px "JetBrains Mono", "Noto Sans TC", monospace'; g.fillText(d.kicker || '', 56, 86);
  g.fillStyle = '#fff'; let fs = 104; g.font = `900 ${fs}px "Noto Sans TC", sans-serif`;
  const titleLines = () => wrapLines(g, d.title, W * .6, 2);
  while ((titleLines().length > 1 || g.measureText(d.title).width > W * .6) && fs > 66) { fs -= 4; g.font = `900 ${fs}px "Noto Sans TC", sans-serif`; }
  const tl = titleLines();
  let y = tl.length > 1 ? 210 : 300;
  tl.forEach((l, k) => g.fillText(l, 56, y + k * (fs * 1.12)));
  y += (tl.length - 1) * fs * 1.12;
  g.fillStyle = '#F5B800'; g.fillRect(56, y + 34, 90, 8);
  g.fillStyle = 'rgba(255,255,255,.82)'; g.font = '500 28px "Noto Sans TC", sans-serif';
  wrapLines(g, d.desc || '', W * .52, 2).forEach((l, k) => g.fillText(l, 56, y + 100 + k * 42));
  g.fillStyle = 'rgba(255,255,255,.95)'; g.font = '700 28px "Noto Sans TC", sans-serif';
  g.fillText(d.foot || '', 56, H - 56);
  const sheen = g.createLinearGradient(0, 0, 0, H * .5);
  sheen.addColorStop(0, 'rgba(255,255,255,.12)'); sheen.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = sheen; g.fillRect(0, 0, W, H * .5);
  g.restore();
  rr(g, 2, 2, W - 4, H - 4, 25); g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = 3; g.stroke();
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  return tex;
}
function shadowTexture() {
  const c = document.createElement('canvas'); c.width = 256; c.height = 160; const g = c.getContext('2d');
  g.filter = 'blur(18px)'; g.fillStyle = 'rgba(0,0,0,.55)'; rr(g, 34, 34, 188, 92, 12); g.fill();
  return new THREE.CanvasTexture(c);
}
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

export function mountStack(DATA, opts = {}) {
  const canvas = document.getElementById('stage');
  const tip = document.getElementById('tip');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const N = DATA.length;
  const api = { focus() {}, blur() {} };
  window.J3M3D = api;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) {
    document.documentElement.classList.add('no-3d');
    return api;
  }
  renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth < 900 ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  camera.position.set(0, 0, 14);
  const world = new THREE.Group(); scene.add(world);

  /* 星塵 */
  const SN = innerWidth < 900 ? 400 : 900, sp = new Float32Array(SN * 3);
  for (let i = 0; i < SN; i++) { sp[i * 3] = (Math.random() - .5) * 40; sp[i * 3 + 1] = (Math.random() - .5) * 24; sp[i * 3 + 2] = -Math.random() * 20 - 2; }
  const starGeo = new THREE.BufferGeometry(); starGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  const starMat = new THREE.PointsMaterial({ color: 0xF5B800, size: 0.05, transparent: true, opacity: 0.5, depthWrite: false });
  const stars = new THREE.Points(starGeo, starMat); scene.add(stars);

  /* 斜向層疊：u = 0 在左下最前，往右上越來越遠；整疊以中間那張為中心 */
  const CW = 3.3, CH = CW * 640 / 1024;
  const C = (N - 1) / 2;
  const cardGeo = new THREE.PlaneGeometry(CW, CH);
  const shGeo = new THREE.PlaneGeometry(CW * 1.25, CH * 1.3);
  const shTex = shadowTexture();
  const BASE_RY = -0.62, BASE_RX = -0.06;
  const path = (u, out) => out.set(1.05 * (u - C), 0.78 * (u - C), 1.6 - u * 1.55 + Math.max(0, 6 - N) * 0.5);
  const cards = [];
  function build() {
    DATA.forEach((d, i) => {
      const holder = new THREE.Group();
      const mesh = new THREE.Mesh(cardGeo, new THREE.MeshBasicMaterial({ map: cardTexture(d), transparent: true }));
      mesh.userData.index = i;
      const sh = new THREE.Mesh(shGeo, new THREE.MeshBasicMaterial({ map: shTex, transparent: true, depthWrite: false, opacity: .6 }));
      sh.position.set(0.12, -0.12, -0.06);
      holder.add(sh, mesh); world.add(holder);
      cards.push({ holder, mesh, sh, d, pull: 0 });
    });
  }

  /* 狀態：卡片少於 5 張時不輪播，固定排開 */
  const loop = N >= 5;
  let pos = 0, target = 0, vel = 0, dragging = false, moved = 0, lastX = 0, lastY = 0, idle = 0;
  let hovered = -1, mx = 0, my = 0, scrollP = 0;
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), v = new THREE.Vector3();
  const wrap = x => ((x % N) + N) % N;
  api.focus = i => { if (loop) { const d = wrap(i - target + 0.5) - 0.5; target += d; } idle = -3; hovered = i; };
  api.blur = () => { hovered = -1; };

  function layout() {
    const w = innerWidth, h = innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const hw = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.position.z * camera.aspect;
    if (w < 900) {
      const sc = Math.min(0.46, w / 820) * (N < 5 ? 1.25 : 1);
      world.position.set(0.75 * sc, 2.2 + 0.34 * sc, 0); world.scale.setScalar(sc);
    } else {
      const ht = document.querySelector('.hero-text');
      const textR = (ht ? ht.getBoundingClientRect().right : w * .5) - 60;
      const left = (textR / w * 2 - 1) * hw;
      const sc = Math.max(0.7, Math.min(1.05, (hw - left) / 7.2));
      world.position.set(left + 5.05 * sc, 0.34 * sc, 0); world.scale.setScalar(sc);
    }
  }
  addEventListener('resize', layout);

  function applyTheme() {
    const light = window.j3mTheme && window.j3mTheme() === 'light';
    starMat.color.set(light ? 0x8F6A08 : 0xF5B800); starMat.opacity = light ? 0.3 : 0.5;
  }
  addEventListener('j3m-theme', applyTheme);
  matchMedia('(prefers-color-scheme: light)').addEventListener('change', applyTheme);

  /* 互動 */
  function pick(e) {
    ndc.set(e.clientX / innerWidth * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects(cards.filter(c => c.holder.visible).map(c => c.mesh), false)[0];
    return hit ? hit.object.userData.index : -1;
  }
  function showTip(i, e) {
    if (i < 0) { tip.classList.remove('show'); canvas.style.cursor = loop ? (dragging ? 'grabbing' : 'grab') : 'default'; return; }
    const t = DATA[i].tip || {};
    tip.innerHTML = `<b>${esc(t.title || DATA[i].title)}</b>${esc(t.body || DATA[i].desc || '')}<span class="go">${esc(t.go || '點擊開啟 →')}</span>`;
    tip.style.left = Math.min(e.clientX, innerWidth - 300) + 'px';
    tip.style.top = Math.min(e.clientY, innerHeight - 180) + 'px';
    tip.classList.add('show'); canvas.style.cursor = 'pointer';
  }
  function open(i) {
    const d = DATA[i];
    if (!d.href) return;
    if (d.ext) window.open(d.href, '_blank', 'noopener');
    else location.href = d.href;
  }
  canvas.addEventListener('pointerdown', e => { dragging = true; moved = 0; lastX = e.clientX; lastY = e.clientY; vel = 0; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', e => {
    mx = e.clientX / innerWidth * 2 - 1; my = e.clientY / innerHeight * 2 - 1;
    if (dragging) {
      const dx = e.clientX - lastX, dy = e.clientY - lastY; lastX = e.clientX; lastY = e.clientY;
      moved += Math.abs(dx) + Math.abs(dy);
      if (loop) { vel = -(dx - dy) * 0.004; target += vel; }
      idle = -2;
      if (moved > 6) { hovered = -1; showTip(-1, e); }
      return;
    }
    if (e.pointerType === 'mouse') { hovered = pick(e); if (hovered >= 0) idle = -1.5; showTip(hovered, e); }
  });
  canvas.addEventListener('pointerup', e => { dragging = false; if (moved < 6) { const i = pick(e); if (i >= 0) open(i); } });
  canvas.addEventListener('pointercancel', () => { dragging = false; });
  canvas.addEventListener('pointerleave', e => { if (!dragging) { hovered = -1; showTip(-1, e); } });
  addEventListener('pointermove', e => { mx = e.clientX / innerWidth * 2 - 1; my = e.clientY / innerHeight * 2 - 1; }, { passive: true });
  function onScroll() {
    scrollP = Math.min(3, scrollY / innerHeight);
    canvas.style.opacity = Math.max(0.35, Math.min(1, 1 - (scrollP - 0.5) * 0.7)).toFixed(3);
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* 動畫 */
  const clock = new THREE.Clock();
  const smooth = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05), time = clock.elapsedTime;
    idle += dt;
    if (loop && !dragging && !reduce && idle > 0 && hovered < 0) target += dt * 0.09;
    if (!dragging) { target += vel; vel *= 0.9; }
    pos += (target - pos) * Math.min(1, dt * 4);
    const s = reduce ? 0 : scrollP;

    cards.forEach((c, i) => {
      let u, vis = 1;
      if (loop) {
        u = wrap(i - pos - s * 0.8 + 0.6) - 0.6;
        vis = smooth(-0.6, 0, u) * smooth(N - 0.6, N - 1.3, u);
      } else u = i;
      c.holder.visible = vis > 0.01;
      c.pull += ((hovered === i ? 1 : 0) - c.pull) * Math.min(1, dt * 9);
      const p = c.pull;
      path(u, v);
      // 抽出：往上、往前滑出整疊卡片，並轉正面對鏡頭
      c.holder.position.set(v.x - 0.7 * p, v.y + 1.0 * p + Math.sin(time * 0.8 + i) * 0.03, v.z + 2.4 * p);
      c.holder.rotation.set(BASE_RX * (1 - p), BASE_RY * (1 - p * 0.75), 0.02 * (1 - p));
      c.holder.scale.setScalar(1 + p * 0.06);
      c.mesh.material.opacity = vis;
      c.sh.material.opacity = vis * (0.55 + p * 0.25);
      c.sh.position.set(0.12 + p * 0.25, -0.12 - p * 0.3, -0.06 - p * 0.2);
    });
    stars.rotation.y += dt * 0.008;

    const px = reduce ? 0 : mx * 0.7, py = reduce ? 0 : -my * 0.45;
    camera.position.x += (px - camera.position.x) * 0.05;
    camera.position.y += (py - s * 0.5 - camera.position.y) * 0.05;
    camera.position.z += (14 + s * 2 - camera.position.z) * 0.06;
    camera.lookAt(0, -s * 0.3, 0);

    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }

  layout();
  const text = DATA.map(d => d.kicker + d.title + d.desc + d.foot).join('');
  (document.fonts ? Promise.all([
    document.fonts.load('900 104px "Noto Sans TC"', text),
    document.fonts.load('500 28px "Noto Sans TC"', text),
    document.fonts.load('700 34px "JetBrains Mono"', '0123456789/·ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  ]).catch(() => {}) : Promise.resolve()).then(() => {
    build(); applyTheme();
    canvas.style.cursor = loop ? 'grab' : 'default';
    frame();
  });

  /* 頁面上的 HTML 卡片：滑過時讓對應的 3D 卡抽出 */
  document.querySelectorAll('[data-stack]').forEach(el => {
    el.addEventListener('pointerenter', () => api.focus(+el.getAttribute('data-stack')));
    el.addEventListener('pointerleave', () => api.blur());
  });
  return api;
}
