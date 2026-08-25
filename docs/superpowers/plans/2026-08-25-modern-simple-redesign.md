# Yukfo.com 现代极简改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 yukfo.com 从 5 页内容型站改版为 4 页现代极简站（Home 左文右图 hero + 精选案例 / Services 精简 / Work 案例集 / Contact 含 FAQ 折叠），全站用真实产品图建立信任。

**Architecture:** 纯静态 HTML/CSS/少量 JS（无框架，现有体系不变）。root 与 public/ 双份同步，Cloudflare 拖拽部署。验证手段 = scripts/check_copy.py（文案铁律）+ 本地预览（scripts/serve_local.py :8897）+ root/public 一致性 diff。

**Tech Stack:** HTML5 / CSS3（自定义 Design System）/ 原生 JS（main.js）/ Python 校验脚本

**Spec:** `docs/superpowers/specs/2026-08-25-modern-simple-redesign-design.md`

## Global Constraints

- 文案铁律：不暗示自有工厂（无 "my own production"）；MOQ/交期不写数字；正文零破折号（`—`/`–`）；`<title>` 里的 `—` 合规
- 品牌色：深蓝 `#1e3a5f`（`--blue`），点缀金黄（现有 `--gold`）；白底
- 导航统一 4 项：Home / Services / Work / Contact（所有页面含 thanks.html）
- 真实图目录：`assets/images/work/`（7 张已入库，1200×900，4:3）
- 每任务结束跑 `python -X utf8 scripts/check_copy.py`（相关页），0 错误才算过
- root 与 public/ 必须最终一致（`diff -r` 校验）
- 表单 FormSubmit 配置（action/_subject/_template/_next/_autoresponse）原样保留
- BR No. 占位行 + 注释保留不动（等用户证书核验）

---

### Task 1: CSS 视觉系统升级（现代圆角 + 新组件）

**Files:**
- Modify: `assets/css/style.css`

**Interfaces:**
- Produces: `--radius:12px`（Design System 全局）、`.hero-split`、`.hero-split .hero-text/.hero-img`、`.case-grid`、`.case-card`、`.lightbox`、`.footer-line` 样式类；保留全部现有类（`.spec-table` `.faq-item` `.case-meta` `.matrix` 等）

- [ ] **Step 1: 修改 `:root` 圆角变量（2px → 12px）**

```css
  --radius:12px;
```

- [ ] **Step 2: 追加新组件样式（文件末尾）**

```css
/* ============ Modern Minimal (2026-08-25) ============ */
/* split hero: left text, right image */
.hero-split{padding:88px 0 72px}
.hero-split .container{display:flex;align-items:center;gap:56px}
.hero-split .hero-text{flex:1.15;min-width:0}
.hero-split h1{font-size:clamp(34px,4.5vw,52px);font-weight:700;line-height:1.12;letter-spacing:-.02em;max-width:600px}
.hero-split .sub{font-size:1.05rem;color:var(--gray);max-width:440px;margin:22px 0 34px;line-height:1.65}
.hero-split .hero-img{flex:1}
.hero-split .hero-img img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;box-shadow:0 18px 44px rgba(30,58,95,.16)}
/* case grid: clean 3-col photo wall */
.case-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.case-card{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--bg);cursor:zoom-in;transition:transform .25s ease,box-shadow .25s ease}
.case-card:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(0,0,0,.08)}
.case-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;transition:transform .35s ease}
.case-card:hover img{transform:scale(1.03)}
.case-card .c-body{padding:16px 18px 18px}
.case-card h3{font-size:1rem;margin-bottom:4px}
.case-card .c-tag{font-size:.75rem;color:var(--gold-deep);font-weight:600;letter-spacing:.03em}
.case-card p{font-size:.86rem;color:var(--gray);margin-top:8px;line-height:1.55}
/* lightbox */
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.88);display:none;align-items:center;justify-content:center;z-index:999;cursor:zoom-out;padding:24px}
.lightbox img{max-width:min(1080px,92vw);max-height:88vh;border-radius:8px}
.lightbox .lb-close{position:absolute;top:14px;right:22px;font-size:2.1rem;color:#fff;background:none;border:none;cursor:pointer;line-height:1}
.lightbox.open{display:flex}
/* footer one-liner */
.footer-line{border-top:1px solid var(--line);padding:22px 0;color:var(--gray);font-size:.85rem;text-align:center}
.footer-line a{color:var(--gray)}
.footer-line a:hover{color:var(--blue)}
@media(max-width:1024px){.hero-split .container{gap:36px}.hero-split h1{font-size:2.2rem}}
@media(max-width:768px){
  .hero-split{padding:56px 0 48px}
  .hero-split .container{flex-direction:column}
  .hero-split .hero-img{width:100%}
  .case-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:480px){.case-grid{grid-template-columns:1fr}}
```

- [ ] **Step 3: 验证 CSS 无语法错误**

Run: `python -X utf8 -c "import re; s=open('assets/css/style.css',encoding='utf-8').read(); print('braces ok' if s.count('{')==s.count('}') else 'MISMATCH')"`
Expected: `braces ok`

- [ ] **Step 4: Commit**

```bash
git add assets/css/style.css
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "style: modern minimal design system (radius 12px, split hero, case grid, lightbox)"
```

---

### Task 2: index.html 重构（左文右图 hero + 精选案例）

**Files:**
- Modify: `index.html`（整个 `<main>` 替换 + nav 改 4 项）

**Interfaces:**
- Consumes: Task 1 的 `.hero-split` `.case-grid` `.footer-line`
- Produces: 新首页结构（供 Task 7 预览验收）

- [ ] **Step 1: nav 改 4 项（第 23-28 行替换）**

```html
    <nav class="nav" aria-label="Main navigation">
      <a href="index" class="active">Home</a>
      <a href="services">Services</a>
      <a href="work">Work</a>
      <a href="contact">Contact</a>
    </nav>
```

- [ ] **Step 2: 替换 `<main>` 全部内容（34-98 行）为新结构**

```html
<main>
  <section class="hero-split">
    <div class="container">
      <div class="hero-text">
        <h1>Need something from China? I'm your sourcing agent. <span style="color:var(--gold-deep)">No category limits.</span></h1>
        <p class="sub">From a single part to a full product line. I find it, verify it, and deliver it.</p>
        <a class="btn" href="contact">Start a Project</a>
        <a class="btn btn-ghost" href="https://wa.me/8617860570306" target="_blank" rel="noopener" style="margin-left:10px">WhatsApp</a>
        <!-- 占位：BR No. 12345678 待替换为真实号（候选 80477500，2026-08-23 第三方目录验证，需用户注册证书核验） -->
        <p style="margin-top:18px;color:var(--gray);font-size:.82rem">Yukfo Limited · Hong Kong · BR No. 12345678</p>
      </div>
      <div class="hero-img"><img src="assets/images/work/work-mold-and-bottle.jpg" alt="Injection mold with its molded bottle"></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Recent Work</h2>
      <div class="case-grid">
        <div class="case-card"><img src="assets/images/work/work-mold-and-bottle.jpg" alt="Injection mold and molded bottle"><div class="c-body"><span class="c-tag">INJECTION MOLDING</span><h3>Mold &amp; Bottle</h3></div></div>
        <div class="case-card"><img src="assets/images/work/work-plastic-parts.jpg" alt="Colored plastic parts"><div class="c-body"><span class="c-tag">CUSTOM PLASTIC</span><h3>Plastic Parts</h3></div></div>
        <div class="case-card"><img src="assets/images/work/work-precision-metal.jpg" alt="Precision metal parts"><div class="c-body"><span class="c-tag">METAL FABRICATION</span><h3>Precision Metal</h3></div></div>
      </div>
      <p style="margin-top:26px"><a class="btn btn-ghost" href="work">See All Work</a></p>
    </div>
  </section>
</main>

<footer class="site-footer footer-line">
  <div class="container">
    <span>© 2026 YUKFO · Yukfo Limited, Hong Kong · <a href="mailto:jesus@yukfo.com">jesus@yukfo.com</a> · <a href="https://wa.me/8617860570306" target="_blank" rel="noopener">WhatsApp</a></span>
  </div>
</footer>
```

- [ ] **Step 3: 验证 check_copy 通过**

Run: `python -X utf8 scripts/check_copy.py --page index`
Expected: `index.html: PASS`；无违禁词、无破折号、`No category limits` 必备事实在

- [ ] **Step 4: Commit**

```bash
git add index.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: home redesign — split hero + featured work (3 real product photos)"
```

---

### Task 3: work.html 新建（案例集 + lightbox）

**Files:**
- Create: `work.html`
- Modify: `assets/js/main.js`（追加 lightbox JS）

**Interfaces:**
- Consumes: Task 1 的 `.case-grid` `.case-card` `.lightbox`；`assets/images/work/` 7 张图
- Produces: `work.html`（canonical `/work`）+ main.js lightbox（供 contact/thanks 的 nav 链接）

- [ ] **Step 1: main.js 追加 lightbox（文件末尾）**

```js
/* lightbox for Work page */
document.addEventListener('click', function(e){
  var card = e.target.closest('.case-card[data-img]');
  if(!card) return;
  var box = document.getElementById('lightbox');
  if(!box){
    box = document.createElement('div');
    box.id = 'lightbox';
    box.className = 'lightbox';
    box.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">&times;</button>';
    document.body.appendChild(box);
    box.addEventListener('click', function(){ box.classList.remove('open'); });
    box.querySelector('.lb-close').addEventListener('click', function(){ box.classList.remove('open'); });
  }
  box.querySelector('img').src = card.getAttribute('data-img');
  box.classList.add('open');
});
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){ var box = document.getElementById('lightbox'); if(box) box.classList.remove('open'); }
});
```

- [ ] **Step 2: 创建 `work.html`**（完整文件，case-meta 数据来自旧 deliveries.html 的真实内容）

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Work — Real Products, Delivered | YUKFO</title>
<meta name="description" content="Real projects delivered by YUKFO: injection molded parts, precision metal parts, rotomolded kayaks, blind systems, extruded profiles, and more. Photos of real work, shipped to clients overseas.">
<meta property="og:title" content="Work — YUKFO">
<meta property="og:description" content="Real projects, delivered. Photos of actual parts and products shipped to clients overseas.">
<meta property="og:type" content="website">
<link rel="canonical" href="https://yukfo.com/work">
<link rel="icon" type="image/jpeg" href="assets/images/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index"><img src="assets/images/logo.jpg" alt="YUKFO logo"><span>YUKFO</span></a>
    <nav class="nav" aria-label="Main navigation">
      <a href="index">Home</a>
      <a href="services">Services</a>
      <a href="work" class="active">Work</a>
      <a href="contact">Contact</a>
    </nav>
    <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
  </div>
</header>

<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Work</h2>
      <p class="lead">Photos of real parts and products from delivered projects. Client names stay confidential, but references are available on request.</p>
      <div class="case-grid">
        <div class="case-card" data-img="assets/images/work/work-mold-and-bottle.jpg"><img src="assets/images/work/work-mold-and-bottle.jpg" alt="Injection mold with molded bottle"><div class="c-body"><span class="c-tag">INJECTION MOLDING</span><h3>Mold &amp; Bottle</h3><div class="case-meta"><span class="m"><b>Process:</b> injection molding, mold development</span><span class="m"><b>Part:</b> custom bottle with tooling</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-plastic-parts.jpg"><img src="assets/images/work/work-plastic-parts.jpg" alt="Colored plastic parts"><div class="c-body"><span class="c-tag">CUSTOM PLASTIC</span><h3>Plastic Parts</h3><div class="case-meta"><span class="m"><b>Material:</b> PA6, ABS, PP</span><span class="m"><b>Process:</b> injection molding</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-precision-metal.jpg"><img src="assets/images/work/work-precision-metal.jpg" alt="Precision metal parts"><div class="c-body"><span class="c-tag">METAL FABRICATION</span><h3>Precision Metal</h3><div class="case-meta"><span class="m"><b>Material:</b> carbon steel, stainless steel</span><span class="m"><b>Process:</b> stamping, bending, laser cutting</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-electrical-panel.jpg"><img src="assets/images/work/work-electrical-panel.jpg" alt="Electrical switch panel and components"><div class="c-body"><span class="c-tag">PROJECT PARTS</span><h3>Switch Panel &amp; Components</h3><div class="case-meta"><span class="m"><b>Part:</b> switch panels, camera modules</span><span class="m"><b>Process:</b> sourcing, assembly, testing</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-metal-assembly.jpg"><img src="assets/images/work/work-metal-assembly.jpg" alt="Metal assembly with brackets and fasteners"><div class="c-body"><span class="c-tag">METAL ASSEMBLY</span><h3>Metal Assemblies</h3><div class="case-meta"><span class="m"><b>Part:</b> brackets, fasteners, assemblies</span><span class="m"><b>Finish:</b> powder coating</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-factory-line.jpg"><img src="assets/images/work/work-factory-line.jpg" alt="Production line at a partner factory"><div class="c-body"><span class="c-tag">PARTNER FACTORY</span><h3>Production Line</h3><div class="case-meta"><span class="m"><b>Process:</b> QC checks at partner factories</span><span class="m"><b>Result:</b> checked and tested before shipping</span></div></div></div>
        <div class="case-card" data-img="assets/images/work/work-bumper.jpg"><img src="assets/images/work/work-bumper.jpg" alt="Automotive bumper part"><div class="c-body"><span class="c-tag">AUTOMOTIVE</span><h3>Bumper Part</h3><div class="case-meta"><span class="m"><b>Material:</b> metal</span><span class="m"><b>Process:</b> forming, finishing</span></div></div></div>
      </div>
      <div class="case-meta" style="margin-top:30px"><span class="m"><b>Programs:</b> 26-SKU blind system · rotomolded kayaks (LLDPE) · window &amp; door profiles (aluminum 6063, PVC) · water tanks · planters · EVA/IXPE foam panels</span></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Start a New Project</h2>
      <p class="lead">Every project above started with a drawing and a question. Send yours.</p>
      <a class="btn" href="contact">Start Your Project</a>
    </div>
  </section>
</main>

<footer class="site-footer footer-line">
  <div class="container">
    <span>© 2026 YUKFO · Yukfo Limited, Hong Kong · <a href="mailto:jesus@yukfo.com">jesus@yukfo.com</a> · <a href="https://wa.me/8617860570306" target="_blank" rel="noopener">WhatsApp</a></span>
  </div>
</footer>
</body>
</html>
```

- [ ] **Step 3: 验证**

Run: `python -X utf8 scripts/check_copy.py --page work`
Expected: `work.html: PASS`（词数无基线跳过带检查；无违禁词/破折号/href 问题）

Run: `python -X utf8 -c "import re; s=open('assets/js/main.js',encoding='utf-8').read(); print('js ok' if s.count('{')==s.count('}') else 'MISMATCH')"`
Expected: `js ok`

- [ ] **Step 4: Commit**

```bash
git add work.html assets/js/main.js
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: Work page — real product photo gallery with lightbox + case meta"
```

---

### Task 4: services.html 精简

**Files:**
- Modify: `services.html`（nav 4 项 + `<main>` 重构）

**Interfaces:**
- Consumes: Task 1 的 `.spec-table` `.qstep` `.matrix`（保留）
- Produces: 精简后 Services（含"为什么不直接找工厂"新节）

- [ ] **Step 1: nav 改 4 项**（同 Task 2 Step 1 的 nav，去掉 Deliveries/FAQ，active 指向 services）

- [ ] **Step 2: 替换 `<main>`（34-138 行）为精简结构**

```html
<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>What I Do</h2>
      <p class="lead">Three ways to work with me. A drawing or a rough idea is all it takes. Most projects start with a sample or a trial run, then move into production.</p>
      <div class="grid">
        <div class="card"><span class="tag">Product Sourcing</span><h3>Anything You Need</h3><p>You name it, I source it: standard or custom components, finished goods, tools, hardware. Prices compared across suppliers, samples verified and factories checked before your money moves.</p></div>
        <div class="card"><span class="tag">Custom Manufacturing</span><h3>Parts Made to Order</h3><p>Injection molding, rotomolding, extrusion, foam die-cutting, metal fabrication. Made in partner factories, with molds developed and validated before production starts.</p></div>
        <div class="card"><span class="tag">Turnkey Delivery</span><h3>Project Management</h3><p>Sourcing, prototyping, production, QC, documents, shipping: end to end, all of it. One contact: me.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Processes at a Glance</h2>
      <p class="lead">Each process suits certain parts and materials, and has its own limits. Use the table to see which one fits your product.</p>
      <div class="table-scroll"><table class="spec-table">
        <tr><th>Process</th><th>Good For</th><th>Materials</th><th>Finishes</th><th>Limits</th></tr>
        <tr><td>Injection Molding</td><td>Pulleys, enclosures, brackets, hardware, housings</td><td>PA6, ABS, PP</td><td>n/a</td><td>Mold cost per part; geometry must allow ejection</td></tr>
        <tr><td>Rotational Molding</td><td>Kayaks, tanks, coolers, planters, large hollow parts</td><td>LLDPE, PP</td><td>n/a</td><td>Hollow parts only; wall thickness varies with rotation</td></tr>
        <tr><td>Plastic Extrusion</td><td>Window and door profiles, trims, rails, structural sections</td><td>PVC, ABS</td><td>n/a</td><td>Constant cross-section along the length</td></tr>
        <tr><td>Aluminum Extrusion</td><td>Window and door systems, rails, frames</td><td>Aluminum 6063</td><td>Anodizing (natural, black), powder coating, dye</td><td>Constant cross-section; bending after extrusion where needed</td></tr>
        <tr><td>Foam Die-Cutting</td><td>Mats, gaskets, panels, packaging, insulation</td><td>EVA, IXPE</td><td>n/a</td><td>Flat sheet parts, cut in 2D</td></tr>
        <tr><td>Metal Fabrication</td><td>Brackets, plates, handles, locks, frames</td><td>Carbon steel, stainless steel, zinc alloys</td><td>Powder coating, anodizing</td><td>Stamping needs tooling; laser cutting works best on flat sheet</td></tr>
      </table></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Materials</h2>
      <p class="lead">The materials behind delivered projects, with the processes and finishes that suit each one. Not sure what to use? Send the drawing or idea and I'll recommend a material and process together.</p>
      <div class="table-scroll"><table class="spec-table">
        <tr><th>Material</th><th>Type</th><th>Typical Applications</th><th>Available Processes</th><th>Finishes</th><th>Notes</th></tr>
        <tr><td>PA6 (Nylon)</td><td>Plastic</td><td>Pulleys, bushings, clips, wear parts</td><td>Injection molding</td><td>n/a</td><td>Tough and wear-resistant; absorbs moisture and needs drying before molding</td></tr>
        <tr><td>ABS</td><td>Plastic</td><td>Enclosures, brackets, handles, hardware</td><td>Injection molding, extrusion</td><td>Paint, texture</td><td>Good impact strength and surface finish</td></tr>
        <tr><td>PP (Polypropylene)</td><td>Plastic</td><td>Tanks, caps, hinges, chemical-resistant parts</td><td>Injection molding, rotomolding</td><td>n/a</td><td>Lightweight, chemical-resistant, low cost per part</td></tr>
        <tr><td>PVC</td><td>Plastic</td><td>Window and door profiles, trims, structural sections</td><td>Extrusion</td><td>n/a</td><td>Rigid profiles with tight tolerances, custom lengths</td></tr>
        <tr><td>EVA / IXPE Foam</td><td>Foam</td><td>Panels, mats, gaskets, packaging, insulation</td><td>Die-cutting</td><td>n/a</td><td>Adhesive-backed options, precision cut shapes</td></tr>
        <tr><td>Aluminum 6063</td><td>Metal</td><td>Window and door systems, rails, structural profiles</td><td>Extrusion, bending</td><td>Anodizing (natural, black), powder coating, dye</td><td>Excellent for extrusion; the 6063 grade is made for it</td></tr>
        <tr><td>Zinc Alloys</td><td>Metal</td><td>Die-cast brackets, housings, locks, handles</td><td>Zinc die-casting</td><td>Paint, plating</td><td>Complex shapes with thin walls in one step</td></tr>
        <tr><td>Carbon &amp; Stainless Steel</td><td>Metal</td><td>Brackets, plates, stamped hardware, frames</td><td>Stamping, bending, laser cutting</td><td>Powder coating</td><td>Strength for structural parts; powder coat protects against rust</td></tr>
      </table></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Why Not Directly a Factory?</h2>
      <p class="lead">Finding a factory is the easy part. The work is in comparing quotes, checking samples, chasing schedules, and catching problems before they ship. A sourcing agent answers for the whole chain: one contact, itemized quotes, and real cost data behind every number.</p>
      <a class="btn" href="contact">Start a Project</a>
    </div>
  </section>
</main>

<footer class="site-footer footer-line">
  <div class="container">
    <span>© 2026 YUKFO · Yukfo Limited, Hong Kong · <a href="mailto:jesus@yukfo.com">jesus@yukfo.com</a> · <a href="https://wa.me/8617860570306" target="_blank" rel="noopener">WhatsApp</a></span>
  </div>
</footer>
```

- [ ] **Step 3: 验证**

Run: `python -X utf8 scripts/check_copy.py --page services`
Expected: `services.html: PASS`；必备事实 PA6/ABS/PP/EVA/IXPE 在；词数较旧基线 776 明显下降（带内或手动记录新词数供 Task 6 重校）

- [ ] **Step 4: Commit**

```bash
git add services.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "refactor: services page trimmed to essentials (capabilities, process table, materials, why-not-factory)"
```

---

### Task 5: contact.html 加 FAQ 折叠 + 删 faq/deliveries + thanks nav

**Files:**
- Modify: `contact.html`（nav 4 项 + 追加 FAQ 折叠区）
- Delete: `faq.html`, `deliveries.html`（root + public）
- Modify: `thanks.html`（nav 4 项）

**Interfaces:**
- Consumes: Task 1 的 `.faq-item`（已有样式）
- Produces: Contact 含 8 问 FAQ；全站 nav 统一

- [ ] **Step 1: contact.html nav 改 4 项**（active 指向 contact）

- [ ] **Step 2: contact.html 表单 section 之后追加 FAQ 区（`</main>` 前）**

```html
  <section class="section">
    <div class="container">
      <h2>Common Questions</h2>
      <details class="faq-item"><summary>Who is YUKFO?</summary><p>YUKFO is me, a sourcing and manufacturing partner with six years on the front line of cross-border supply chains. One person pushes the whole project forward, straight to the source. The business runs on word of mouth and clients who come back, so every order matters.</p></details>
      <details class="faq-item"><summary>Are you a factory?</summary><p>No. All production runs through partner factories, picked for each project and checked at each stage. Yukfo Limited is registered in Hong Kong, and the work happens on the ground in the Yangtze River Delta. You deal with one accountable person, not a chain of contacts.</p></details>
      <details class="faq-item"><summary>How do you keep pricing transparent?</summary><p>Every quote is itemized line by line: materials, tooling, processing, finishing, logistics. I work from a database of real cost data across factories and processes, so unreasonable quotes stand out and you pay for what the part actually costs, without middleman markup.</p></details>
      <details class="faq-item"><summary>What is your minimum order quantity (MOQ)?</summary><p>It varies by product and by supplier. Tell me your quantity and I'll confirm the MOQ and price together.</p></details>
      <details class="faq-item"><summary>How long does production take?</summary><p>It depends on the supplier and the process. Every quote comes with a dated schedule, and the shipping time is quoted right next to it.</p></details>
      <details class="faq-item"><summary>What payment methods do you accept?</summary><p>Bank transfer (T/T): 30% deposit to start production, 70% before shipment. Payments go to Yukfo Limited (Hong Kong). Sample costs are charged separately and deducted from your first production order.</p></details>
      <details class="faq-item"><summary>Do you charge for samples?</summary><p>Small parts: I often cover the sample cost or charge only the cost price. Large parts (molds, rotomolded items) carry a sample/mold fee, credited back when you place a production order.</p></details>
      <details class="faq-item"><summary>What happens if there is a quality problem?</summary><p>Problems are handled where they show up. If a sample fails, it goes back to the supplier with photos and measurements before anything continues. If inspection catches something mid-production, the fix is agreed before the next batch runs. Everything is documented with photos and test results, so there is a record of what was found and what was done about it.</p></details>
    </div>
  </section>
```

- [ ] **Step 3: contact.html footer 换 footer-line**（同 Task 2 的 footer 结构）

- [ ] **Step 4: 删 faq.html、deliveries.html，统一 thanks.html nav**

```bash
rm faq.html deliveries.html
# thanks.html: nav 内 Deliveries/FAQ 两个 <a> 删除，Work 插入（位置在 Services 后）
```

thanks.html nav（21-27 行附近）替换为：

```html
    <nav class="nav" aria-label="Main navigation">
      <a href="index">Home</a>
      <a href="services">Services</a>
      <a href="work">Work</a>
      <a href="contact">Contact</a>
    </nav>
```

- [ ] **Step 5: 验证**

Run: `python -X utf8 scripts/check_copy.py --page contact`
Expected: `contact.html: PASS`；必备事实 `24 hours` 在

Run: `ls *.html`
Expected: `contact.html  index.html  services.html  thanks.html  work.html`（faq/deliveries 已删）

Run: `python -X utf8 scripts/check_copy.py`
Expected: 5 页全 PASS（faq/deliveries 不在 glob 内，无"页面不存在"错误）

- [ ] **Step 6: Commit**

```bash
git add contact.html thanks.html
git rm faq.html deliveries.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: FAQ folded into Contact (8 questions); remove faq and deliveries pages"
```

---

### Task 6: _redirects / sitemap / check_copy 重校 / public 同步

**Files:**
- Modify: `_redirects`, `sitemap.xml`, `scripts/check_copy.py`
- Sync: root → `public/`

**Interfaces:**
- Consumes: Task 3 的 `work.html`、Task 5 的页面集
- Produces: 可部署的 4 页站（root + public 一致）

- [ ] **Step 1: _redirects 更新**

```text
/index.html / 301
/services.html /services 301
/work.html /work 301
/processes /services 301
/processes.html /services 301
/materials /services 301
/materials.html /services 301
/deliveries /work 301
/deliveries.html /work 301
/faq /contact 301
/faq.html /contact 301
/about /contact 301
/about.html /contact 301
/contact.html /contact 301
```

- [ ] **Step 2: sitemap.xml 更新（4 URL）**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://yukfo.com/</loc><priority>1.0</priority></url>
  <url><loc>https://yukfo.com/services</loc><priority>0.9</priority></url>
  <url><loc>https://yukfo.com/work</loc><priority>0.9</priority></url>
  <url><loc>https://yukfo.com/contact</loc><priority>0.9</priority></url>
</urlset>
```

- [ ] **Step 3: check_copy.py 更新**

MUST_KEEP（第 15-23 行）改为：

```python
MUST_KEEP = {
    'index':    ['No category limits'],
    'services': ['PA6', 'ABS', 'PP', 'EVA', 'IXPE'],
    'work':     ['26 SKUs'],
    'contact':  ['24 hours', '30%', '70%'],
}
```

BASELINE_WORDS（第 24 行）改为（占位，Step 5 实测后回填）：

```python
BASELINE_WORDS = {'index': 90, 'services': 420, 'work': 220, 'contact': 350}
```

- [ ] **Step 4: 同步 public/（root 删除页面也要删）**

```bash
mkdir -p public/assets/images/work
cp index.html services.html work.html contact.html thanks.html public/
cp assets/css/style.css public/assets/css/style.css
cp assets/js/main.js public/assets/js/main.js
cp assets/images/work/*.jpg public/assets/images/work/
cp _redirects sitemap.xml public/
rm -f public/faq.html public/deliveries.html
```

- [ ] **Step 5: 实测词数并回填基线**

Run: `python -X utf8 scripts/check_copy.py`
查看各页输出词数 → 把实际值写入 BASELINE_WORDS（Step 3 的占位值）→ 再跑确认带内

Expected: 全部 PASS，全站合计在带内（0.70-1.10），0 错误 0 警告（或警告人工判定）

- [ ] **Step 6: root/public 一致性 + clean URL 验证**

Run: `diff -r index.html public/index.html && diff -r assets public/assets && diff -r work.html public/work.html`
Expected: 无输出（一致）

Run: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8897/work`
Expected: `200`

- [ ] **Step 7: Commit**

```bash
git add _redirects sitemap.xml scripts/check_copy.py public/ index.html services.html work.html contact.html thanks.html assets/ scripts/ docs/
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "chore: redirects/sitemap/check_copy rebaselined for 4-page site, public/ synced"
```

---

### Task 7: 预览验收 + 8/23 存量提交

**Files:**
- Run: `python -X utf8 scripts/serve_local.py` → http://127.0.0.1:8897

**Interfaces:**
- Consumes: 全部前序任务
- Produces: 用户验收 + git 与线上对齐

- [ ] **Step 1: 本地预览全站**

Run: `python -X utf8 scripts/serve_local.py`（后台）
打开 `http://127.0.0.1:8897` 逐页走查：Home（hero 左文右图/精选 3 图/底部行）、Work（7 图网格 + 点击放大 + Esc 关闭）、Services（表完整）、Contact（表单 + FAQ 折叠展开）、移动端 480px 零溢出

- [ ] **Step 2: 用户验收**

请用户过目 4 页，收集反馈 → 如有修改点返回对应 Task 修复

- [ ] **Step 3: 8/23 已部署存量提交**（让 git 与线上 5 页版对齐，再推改版）

```bash
git add -A
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "chore: commit 8/23 deployed state (page reduction 8->5, conservative UI upgrade) before redesign"
```

- [ ] **Step 4: 最终校验**

Run: `python -X utf8 scripts/check_copy.py`
Expected: 全 PASS
Run: `git status --short`
Expected: 干净（除 .playwright-cli/、docs/hero-variants-preview.html 等 untracked 待处理）

- [ ] **Step 5: 收尾说明（不执行，留给用户/下轮）**

- BR No. 12345678 替换（需证书核验 80477500）
- FormSubmit 激活验证（部署后提交测试表单 → jesus@yukfo.com 点激活邮件）
- 附件上传实测（RQ-9）
- push（走 clash 代理）+ 拖 public/ 部署
