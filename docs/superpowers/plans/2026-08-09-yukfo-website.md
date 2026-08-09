# yukfo.com 官网实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 D:\YUKFO WED 构建 yukfo.com 的 5 页英文静态官网并完成素材准备，为第 4 周部署 Cloudflare Pages 做准备。

**Architecture:** 零依赖纯静态 HTML/CSS/JS。CSS 变量设计系统（极简白 + 深蓝 #1e3a5f + 金黄 #FFC107 系，从 Logo 提取）。5 个独立 HTML 页共享 style.css/main.js。询盘表单用 FormSubmit 免费转发（纯 HTML action，零 JS 依赖），收件邮箱集中在 contact.html 一个位置便于修改。验证方式：本地 http server + agent-browser 截图 + image-viewer 评审（沿用工艺大全的界面评审流程）。

**Tech Stack:** 纯 HTML5/CSS3/vanilla JS；本地预览 python http.server；截图用 playwright-cli/agent-browser；视觉评审用 DashScope qwen3-vl；素材下载 Unsplash CDN 直链 + DashScope 万相文生图；git（无身份配置，提交一律 `git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit`）。

## Global Constraints

- 全英文内容（目标：北美/欧洲/拉美采购商）
- 定位铁律：不展示"自有"机器/车间照片；产品图不扒网；不放阿里国际站/中国制造网链接；不发布价格
- 视觉：极简白底、黑白灰、1px 细线、小圆角 2px、无网格无阴影；深蓝 #1e3a5f 主点缀；金黄 #FFC107 系仅用于 Logo 呼应（克制使用）
- 主题色变量必须定义在 style.css 的 `:root`，页面不得硬编码颜色
- 图片铁律：Industries 页用图库行业示意（标注用途为示意），不冒充自有产品
- 邮箱固定：hkyukfo@outlook.com（contact.html 顶部注释标注"改邮箱只改这里"）
- 导航结构：Home / Services / Industries / About / Contact，当前页高亮
- **阅读体验铁律（用户硬性要求 2026-08-09）**：正文 ≥16px、行高 ≥1.7、正文内容最大宽度 ≤680px（每行 45-75 字符舒适区）、正文对比度 ≥7:1（#1a1a1a on #fff = 17:1 ✓；#6b6b6b on #fff = 5.7:1 ✓；蓝 #1e3a5f on #fff = 10:1 ✓）、标题层级一页一种主次、一屏一个重点、无装饰干扰（已由无阴影无网格保证）
- **文案语言规则（面向非英语母语买家）**：短句（≤20 词）、简单常用词（不用术语缩写）、主动语态、一人称、每段一个意思；Services/Industries 页配"一图一文"结构，文字块不超 80 词
- git 仓库根 = D:\YUKFO WED；每任务完成后提交

---

### Task 1: 项目骨架 + 设计系统

**Files:**
- Create: `D:\YUKFO WED\.gitignore`
- Create: `D:\YUKFO WED\assets\css\style.css`
- Create: `D:\YUKFO WED\assets\js\main.js`

**Interfaces:**
- Produces: CSS 变量 `--blue:#1e3a5f; --blue-light:#2a4d7a; --gold:#ffc107; --gold-deep:#b8860b; --ink:#1a1a1a; --gray:#6b6b6b; --line:#e5e5e5; --bg:#ffffff; --bg-soft:#f7f8fa;`；`main.js` 导出全局函数 `toggleMenu()`；所有页面 `<link rel="stylesheet" href="assets/css/style.css">` + `<script src="assets/js/main.js" defer></script>`

- [ ] **Step 1: git init + .gitignore**

```bash
cd "/d/YUKFO WED" && git init 2>/dev/null; printf 'node_modules/\n.DS_Store\n*.log\n' > .gitignore
```

- [ ] **Step 2: 写设计系统 style.css**

完整内容（唯一真源，后续页面只引用变量）：

```css
/* ============ Design System ============ */
:root{
  --blue:#1e3a5f; --blue-light:#2a4d7a;
  --gold:#ffc107; --gold-deep:#b8860b;
  --ink:#1a1a1a; --gray:#6b6b6b; --line:#e5e5e5;
  --bg:#ffffff; --bg-soft:#f7f8fa;
  --radius:2px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;font-size:16px}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
.container{max-width:1100px;margin:0 auto;padding:0 20px}
/* header */
.site-header{border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:100}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.15rem;color:var(--ink);letter-spacing:.04em}
.brand img{height:32px;width:auto}
.brand:hover{text-decoration:none}
.nav{display:flex;gap:28px}
.nav a{color:var(--ink);font-size:.95rem}
.nav a.active{color:var(--blue);font-weight:600;border-bottom:2px solid var(--blue);padding-bottom:2px}
.menu-toggle{display:none;background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--ink)}
/* hero */
.hero{padding:72px 0 56px;border-bottom:1px solid var(--line)}
.hero h1{font-size:2.3rem;line-height:1.3;font-weight:700;max-width:760px}
.hero p.sub{font-size:1.12rem;color:var(--gray);max-width:640px;margin:18px 0 30px}
.hero .accent{color:var(--blue)}
/* buttons */
.btn{display:inline-block;background:var(--blue);color:#fff!important;padding:12px 26px;border-radius:var(--radius);font-weight:600;font-size:.98rem;border:1px solid var(--blue)}
.btn:hover{background:var(--blue-light);text-decoration:none}
.btn-ghost{background:transparent;color:var(--blue)!important;border:1px solid var(--blue)}
.btn-ghost:hover{background:var(--bg-soft)}
/* sections */
.section{padding:56px 0;border-bottom:1px solid var(--line)}
.section h2{font-size:1.6rem;font-weight:700;margin-bottom:8px}
.section h2::before{content:"";display:inline-block;width:4px;height:1.1em;background:var(--blue);margin-right:10px;vertical-align:-2px}
.section .lead{color:var(--gray);max-width:680px;margin-bottom:32px}
/* reading experience: keep text blocks narrow for comfort */
.card p{max-width:65ch}
.industry p{max-width:65ch}
h1,h2,h3{line-height:1.35}
@media(max-width:760px){body{font-size:16px}} /* never shrink below 16px */
/* cards grid */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.card{border:1px solid var(--line);border-radius:var(--radius);padding:24px;background:var(--bg)}
.card h3{font-size:1.05rem;margin-bottom:10px;color:var(--blue)}
.card p{color:var(--gray);font-size:.95rem}
.card .tag{display:inline-block;font-size:.75rem;color:var(--gold-deep);border:1px solid var(--gold);border-radius:var(--radius);padding:2px 8px;margin-bottom:12px}
/* industry list */
.industry{display:flex;gap:24px;align-items:center;border:1px solid var(--line);border-radius:var(--radius);padding:20px;margin-bottom:20px;background:var(--bg)}
.industry img{width:220px;height:150px;object-fit:cover;border-radius:var(--radius)}
.industry h3{color:var(--blue);margin-bottom:6px}
.industry p{color:var(--gray);font-size:.95rem}
/* contact form */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.field{display:flex;flex-direction:column;gap:6px;margin-bottom:14px}
.field label{font-size:.85rem;font-weight:600}
.field input,.field select,.field textarea{border:1px solid var(--line);border-radius:var(--radius);padding:11px 14px;font:inherit;background:var(--bg)}
.field textarea{min-height:130px;resize:vertical}
.field input:focus,.field textarea:focus{border-color:var(--blue);outline:none}
/* footer */
.site-footer{border-top:1px solid var(--line);padding:28px 0;color:var(--gray);font-size:.88rem;background:var(--bg)}
.footer-inner{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
/* notice */
.notice{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:16px 20px;font-size:.92rem;color:var(--gray);margin-bottom:28px}
.notice b{color:var(--ink)}
/* responsive */
@media(max-width:760px){
  .nav{display:none;position:absolute;top:64px;left:0;right:0;background:var(--bg);border-bottom:1px solid var(--line);flex-direction:column;padding:16px 20px;gap:14px}
  .nav.open{display:flex}
  .menu-toggle{display:block}
  .hero h1{font-size:1.7rem}
  .industry{flex-direction:column;align-items:flex-start}
  .industry img{width:100%;height:auto}
  .form-grid{grid-template-columns:1fr}
}
```

- [ ] **Step 3: 写 main.js**

```js
function toggleMenu(){
  document.querySelector('.nav').classList.toggle('open');
}
document.addEventListener('click', function(e){
  var nav = document.querySelector('.nav');
  if(nav && !nav.contains(e.target) && !e.target.closest('.menu-toggle')) nav.classList.remove('open');
});
```

- [ ] **Step 4: 提交**

```bash
cd "/d/YUKFO WED" && git add .gitignore assets/css/style.css assets/js/main.js && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: design system + skeleton"
```

---

### Task 2: index.html（首页）

**Files:**
- Create: `D:\YUKFO WED\index.html`

**Interfaces:**
- Consumes: Task 1 的 CSS 类（.site-header/.hero/.btn/.section/.grid/.card/.industry/.site-footer/.container/.notice）
- Produces: 其他 4 页复制其 header/footer 结构

- [ ] **Step 1: 写 index.html 完整内容**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YUKFO — Custom Manufacturing & Product Sourcing Partner</title>
<meta name="description" content="YUKFO is your manufacturing partner: custom plastic & metal parts, product sourcing and full project delivery for outdoor, marine and home products. From drawings to delivered goods.">
<meta property="og:title" content="YUKFO — Custom Manufacturing & Product Sourcing Partner">
<meta property="og:description" content="From your drawings to delivered parts. Custom manufacturing, product sourcing, and full project management.">
<meta property="og:type" content="website">
<link rel="icon" type="image/jpeg" href="assets/images/logo.jpg">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html"><img src="assets/images/logo.jpg" alt="YUKFO logo"><span>YUKFO</span></a>
    <nav class="nav" aria-label="Main navigation">
      <a href="index.html" class="active">Home</a>
      <a href="services.html">Services</a>
      <a href="industries.html">Industries</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </nav>
    <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
  </div>
</header>

<main>
  <section class="hero">
    <div class="container">
      <h1>Your project, delivered. <span class="accent">From drawings to finished goods.</span></h1>
      <p class="sub">Custom plastic and metal parts, product sourcing, and full project management — for outdoor, marine, and home products. You bring the idea or the drawing; I make it happen.</p>
      <a class="btn" href="contact.html">Send Your Project</a>
      <a class="btn btn-ghost" href="services.html" style="margin-left:10px">See What I Do</a>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>How I Help</h2>
      <p class="lead">Three ways to work with YUKFO — one person accountable for the whole project, from first quote to delivered goods.</p>
      <div class="grid">
        <div class="card"><span class="tag">Custom Manufacturing</span><h3>Plastic &amp; Metal Parts</h3><p>Injection molding, rotomolding, extrusion, foam die-cutting, metal stamping and fabrication, electronics assembly — produced through trusted partner factories, quality-checked at every stage.</p></div>
        <div class="card"><span class="tag">Product Sourcing</span><h3>Find What You Need</h3><p>Need a component or finished product outside my own processes? I source it for you — the right factory, honest comparison pricing, and verified quality.</p></div>
        <div class="card"><span class="tag">Turnkey Delivery</span><h3>Project Management</h3><p>Material and process advice, transparent cost breakdowns, prototyping, mass production, QC, export documents, and shipping to your door. One point of contact throughout.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Industries I Work With</h2>
      <p class="lead">Real projects, delivered for brands worldwide.</p>
      <div class="grid">
        <div class="card"><h3>Outdoor &amp; Hunting</h3><p>Complete prefabricated blind systems — extrusions, panels, hardware. 26 SKUs engineered and shipped for one product line.</p></div>
        <div class="card"><h3>Water Sports</h3><p>Rotomolded hulls, paddles, and marine accessories — molds, production, and finishing.</p></div>
        <div class="card"><h3>Home &amp; Building</h3><p>Window and door profiles, tanks, decorative planters, EVA foam panels.</p></div>
        <div class="card"><h3>Electronics</h3><p>Control panels, connectors, smart-lock hardware systems, cameras.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Why a One-Person Partner?</h2>
      <p class="lead">My business is my reputation. Every order is a bet on a repeat order — so your interests and mine are the same: the right factory, a fair price, and no surprises.</p>
      <a class="btn" href="about.html">Meet the Person Behind YUKFO</a>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container footer-inner">
    <span>© 2026 YUKFO. Custom manufacturing &amp; sourcing.</span>
    <span><a href="mailto:hkyukfo@outlook.com">hkyukfo@outlook.com</a></span>
  </div>
</footer>
</body>
</html>
```

- [ ] **Step 2: 浏览器验证首页渲染**

```bash
cd "/d/YUKFO WED" && (python -X utf8 -m http.server 8760 >/dev/null 2>&1 &) && sleep 1
curl -s -o /dev/null -w "index: %{http_code}\n" "http://localhost:8760/index.html"
curl -s "http://localhost:8760/assets/css/style.css" | head -3
```

Expected: `index: 200` + CSS 返回 `:root{...}`。浏览器人工抽查后 kill server（`taskkill //F //IM python.exe` 谨慎，用端口杀：`netstat -ano | findstr :8760` 后 `taskkill //PID <pid> //F`）。

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add index.html && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: home page"
```

---

### Task 3: services.html

**Files:**
- Create: `D:\YUKFO WED\services.html`

**Interfaces:**
- Consumes: Task 1 CSS + Task 2 的 header/footer 模板（复制，active 改到 Services）
- Produces: 无

- [ ] **Step 1: 写 services.html（header/footer 与 index 一致，nav active 改为 services.html）**

主体结构（三服务块 + 工艺矩阵）：

```html
<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Custom Manufacturing</h2>
      <p class="lead">My own production processes, run through trusted partner factories with QC at every stage. Tools and molds developed in-house.</p>
      <div class="grid">
        <div class="card"><h3>Injection Molding</h3><p>PA6, ABS, PP and more — precision parts from 1g pulleys to complex enclosures. Molds developed and validated before production.</p></div>
        <div class="card"><h3>Rotational Molding</h3><p>Large hollow parts: kayak hulls, tanks, coolers, planters. Mold design, tooling, and production.</p></div>
        <div class="card"><h3>Plastic Extrusion</h3><p>PVC and ABS profiles for windows, doors, and structural trims — tight tolerances, custom cut lengths.</p></div>
        <div class="card"><h3>Foam Die-Cutting</h3><p>EVA and IXPE foam panels, mats, and gaskets with adhesive backing and precision cutting.</p></div>
        <div class="card"><h3>Metal Fabrication</h3><p>Stamping, aluminum extrusion with bending, laser cutting, zinc die-casting, powder coating — brackets, plates, handles, locks.</p></div>
        <div class="card"><h3>Electronics Assembly</h3><p>Control panels, connectors, cameras, and smart hardware — sourced components, assembled, and tested.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Product Sourcing</h2>
      <p class="lead">If it's outside my own processes, I find it for you. I compare real factories, real prices, and real quality — the same rigor I apply to my own production.</p>
      <ul style="padding-left:20px;color:var(--gray)">
        <li>Standard and custom components: fasteners, magnets, fittings, electronics</li>
        <li>Honest price comparison across suppliers — I know what things should cost</li>
        <li>Sample verification and factory QC before your money moves</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Turnkey Project Delivery</h2>
      <p class="lead">From a drawing to goods on your doorstep — one accountable partner for everything in between.</p>
      <div class="grid">
        <div class="card"><h3>1 · Engineering Advice</h3><p>Material selection, process selection, DFM feedback on your drawings — before you commit to tooling.</p></div>
        <div class="card"><h3>2 · Transparent Pricing</h3><p>Itemized cost breakdowns: materials, tooling amortization, processing, finishing, logistics. No hidden lines.</p></div>
        <div class="card"><h3>3 · Prototyping &amp; Production</h3><p>Samples first, then mass production with scheduled QC checkpoints.</p></div>
        <div class="card"><h3>4 · Export &amp; Delivery</h3><p>Export documents, customs handling, and shipping to your port or door — I've shipped to North America, Europe, and Latin America.</p></div>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 2: 浏览器验证（curl 200 + 人工/截图抽查）**（同 Task 2 Step 2 命令模式）

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add services.html && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: services page"
```

---

### Task 4: industries.html

**Files:**
- Create: `D:\YUKFO WED\industries.html`

**Interfaces:**
- Consumes: Task 1 CSS、Task 2 模板、Task 7 图片（`assets/images/industries/*.jpg`，此任务先写 img 占位 `src` 指向 Task 7 的最终文件名，Task 7 完成后图片自动就位）

- [ ] **Step 1: 写 industries.html（header/footer 模板，active=industries）**

主体（4 个行业块，每块配行业示意图和真实案例要点；img src 指向 Task 7 文件，加载前不阻塞）：

```html
<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Industries</h2>
      <p class="lead">Real projects I've delivered for brands worldwide. If you make or source products in these spaces, we already speak the same language.</p>
      <div class="industry">
        <img src="assets/images/industries/kayak.jpg" alt="Water sports products">
        <div><h3>Water Sports &amp; Marine</h3><p>Rotomolded kayak hulls, paddles and accessories for kayak brands in the US and Europe — molds developed, production managed, quality checked. Trusted by paddle and boat manufacturers.</p></div>
      </div>
      <div class="industry">
        <img src="assets/images/industries/outdoor.jpg" alt="Outdoor products">
        <div><h3>Outdoor &amp; Hunting</h3><p>A complete prefabricated blind system — 26 SKUs of extruded profiles, acrylic panels, injection-molded hardware, stamped steel parts, and EVA foam — engineered, produced, and shipped as one program.</p></div>
      </div>
      <div class="industry">
        <img src="assets/images/industries/home.jpg" alt="Home and building products">
        <div><h3>Home &amp; Building</h3><p>Window and door profiles and hardware, water tanks, decorative planters, and EVA/IXPE foam panels for flooring and insulation.</p></div>
      </div>
      <div class="industry">
        <img src="assets/images/industries/electronics.jpg" alt="Electronics products">
        <div><h3>Electronics</h3><p>DC control switch panels, connectors, surveillance cameras, and smart-lock hardware systems — components sourced, assembled, and tested.</p></div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h2>Have a Product in Mind?</h2>
      <p class="lead">If it's made of plastic, metal, or electronics — or needs to be assembled from them — send me the drawing.</p>
      <a class="btn" href="contact.html">Start the Conversation</a>
    </div>
  </section>
</main>
```

- [ ] **Step 2: 浏览器验证（curl 200）**

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add industries.html && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: industries page"
```

---

### Task 5: about.html

**Files:**
- Create: `D:\YUKFO WED\about.html`

**Interfaces:**
- Consumes: Task 1 CSS、Task 2 模板

- [ ] **Step 1: 写 about.html（active=about）**

主体（个人故事，内容已获用户确认方向）：

```html
<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>About</h2>
      <p class="lead">I'm Jesus — founder of YUKFO. Five years in cross-border trade, serving clients in North America, Latin America, and Europe.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="grid">
        <div class="card"><h3>What I Do</h3><p>I take your idea or drawing and turn it into a delivered product — material and process advice, honest cost breakdowns, prototyping, mass production, quality checks, and shipping to your door.</p></div>
        <div class="card"><h3>Where I've Worked</h3><p>Clients and products shipped to the United States, Canada, Ecuador, Venezuela, and Austria — across hunting equipment, water sports, home products, and electronics.</p></div>
        <div class="card"><h3>Why Work With One Person</h3><p>My whole business is my reputation. Every order is a bet on a repeat order — so your interests and mine are the same: the right factory, a fair price, and no surprises.</p></div>
        <div class="card"><h3>My Edge: Cost Transparency</h3><p>I track real manufacturing costs across factories and processes. When I quote, you get itemized lines — and when a supplier is out of line, I catch it. You pay for what the part should cost, not what a middleman guesses it might.</p></div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h2>Working With Me</h2>
      <p class="lead">No contracts to sign just to ask a question. Send the drawing or idea, and you'll have a response within 24 hours on working days.</p>
      <a class="btn" href="contact.html">Send Your Project</a>
    </div>
  </section>
</main>
```

- [ ] **Step 2: 浏览器验证（curl 200）**

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add about.html && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: about page"
```

---

### Task 6: contact.html + 表单

**Files:**
- Create: `D:\YUKFO WED\contact.html`

**Interfaces:**
- Produces: 表单 POST 到 `https://formsubmit.co/hkyukfo@outlook.com`（FormSubmit 免费档；第一次真实提交后收件邮箱会收到激活邮件，需用户点一次激活——上线前联调时处理）

- [ ] **Step 1: 写 contact.html（active=contact）**

```html
<!-- 收件邮箱：修改只改此表单 action 里的 hkyukfo@outlook.com（以及页脚 mailto） -->
<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Contact</h2>
      <p class="lead">Send your drawing, idea, or question — you'll have a reply within 24 hours on working days.</p>
      <div class="notice"><b>Tip:</b> include quantity, target price if you have one, and delivery date. If you have drawings or specs, mention them and I'll share a secure way to send files.</div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <form action="https://formsubmit.co/hkyukfo@outlook.com" method="POST" class="form-grid">
        <input type="hidden" name="_subject" value="New inquiry from yukfo.com">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <div class="field"><label for="name">Name *</label><input id="name" name="Name" type="text" required></div>
        <div class="field"><label for="email">Email *</label><input id="email" name="Email" type="email" required></div>
        <div class="field"><label for="company">Company</label><input id="company" name="Company" type="text"></div>
        <div class="field"><label for="product">Product / Part Description *</label><textarea id="product" name="Product description" required placeholder="What are we making? Material, size, quantity..."></textarea></div>
        <div class="field"><label for="quantity">Quantity</label><input id="quantity" name="Quantity" type="text"></div>
        <div class="field"><label for="target">Target Price (USD)</label><input id="target" name="Target price" type="text"></div>
        <div class="field"><label for="deadline">Delivery Deadline</label><input id="deadline" name="Delivery deadline" type="text"></div>
        <div style="grid-column:1/-1"><button class="btn" type="submit">Send Inquiry</button></div>
      </form>
    </div>
  </section>
</main>
```

- [ ] **Step 2: 浏览器验证（curl 200；表单字段齐全性人工/截图确认）**

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add contact.html && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: contact page with inquiry form"
```

---

### Task 7: 素材——行业图下载 + AI 生成

**Files:**
- Create: `D:\YUKFO WED\assets\images\industries\{kayak,outdoor,home,electronics}.jpg`
- Create: `D:\YUKFO WED\assets\images\generated\{rotomolding,extrusion}.jpg`（图库缺失时）

**Interfaces:**
- Produces: Task 4 引用的 4 张行业图文件

- [ ] **Step 1: 下载 4 张行业场景图（Unsplash CDN 直链）**

先验证链接可用再保存（每张 curl 到 /dev/null 检查 200），从以下候选按序尝试，失败则换下一组（ID 可执行时从 unsplash.com/napi/search 获取，若 napi 被拒则改用 WebSearch 找 images.unsplash.com 直链）：
- kayak: 搜索 "kayak" → 取宽幅（w=1600）竖构图裁剪为 220×150 由 CSS object-fit 处理
- outdoor: 搜索 "hunting blind" / "outdoor camouflage"
- home: 搜索 "window profile" / "modern home interior"
- electronics: 搜索 "circuit board" / "electronics manufacturing"

下载后记录来源 URL 到 `assets/images/README.md`（素材来源台账，含作者/许可链接）。

- [ ] **Step 2: AI 生成补充图（DashScope 万相）**

若 Step 1 某场景无合适真实图，用 DashScope 文生图生成示意（提示词示例：*"photorealistic industrial rotomolding machine producing a large plastic water tank, clean bright factory, wide shot"*）。脚本保存为 `scripts/gen_image.py`（DASHSCOPE_API_KEY 从环境变量读取，结果轮询 task 状态后下载），输出到 `assets/images/generated/`。

- [ ] **Step 3: 4 张图展示给用户挑选（image-viewer 逐张预览），确认后进入 Task 8**

- [ ] **Step 4: 提交**

```bash
cd "/d/YUKFO WED" && git add assets/images/ && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: industry imagery"
```

---

### Task 8: 全站视觉评审（浏览器截图 + AI 评审迭代）

**Files:**
- Modify: `D:\YUKFO WED\assets\css\style.css`（仅评审发现问题时）

- [ ] **Step 1: 起本地 server（8760），agent-browser 逐页截图**

5 页各截一张（桌面 1280 宽），存 `docs/review/`。

- [ ] **Step 2: image-viewer（qwen3-vl-flash）逐张评审**

检查项：布局错位、颜色硬编码、文字溢出、导航高亮、对比度、移动端（另截 375 宽首页一张）。

- [ ] **Step 3: 修复评审发现的问题（如溢出/对齐/间距），复截复评至通过**

- [ ] **Step 4: 提交**

```bash
cd "/d/YUKFO WED" && git add -A && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "polish: visual review fixes"
```

---

### Task 9: Hero 变体对比 + 用户选定

**Files:**
- Create: `D:\YUKFO WED\docs\review\hero-variants\`（3 个变体的截图与说明）

- [ ] **Step 1: 做 2 个额外 hero 变体（临时在 index.html 上切换样式：A=现版左对齐大字；B=居中+金色点缀线；C=深蓝底白字），分别截图**

- [ ] **Step 2: 变体预览链接/截图给用户，用户选定后固化到 style.css/index.html**

- [ ] **Step 3: 提交**

```bash
cd "/d/YUKFO WED" && git add -A && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: finalize hero design"
```

---

### Task 10: 部署准备（Cloudflare Pages 指南 + 检查清单）

**Files:**
- Create: `D:\YUKFO WED\docs\DEPLOY.md`

- [ ] **Step 1: 写 DEPLOY.md**（部署操作手册，上线周 W4 执行）：

内容要点（完整写入手册）：
1. Cloudflare 注册（免费）→ dashboard 新建 Pages 项目 → 上传目录模式（直接拖入 index.html + assets/ 目录）或连接 GitHub
2. Namecheap 操作（用户执行，逐步引导）：关闭 URL Forwarding 停靠 → Domain List → Advanced DNS → 删除旧 A 记录 → 按 Cloudflare Pages 提供的自定义域名提示添加 CNAME `www` → Namecheap 的 Nameservers 改为 Cloudflare 分配的两个 NS（如需）
3. 验证：`curl -I https://yukfo.com` 返回 200 + CF-Ray 头；https://www.yukfo.com 与裸域均可访问
4. 表单联调：真实提交一次询盘 → 收件邮箱收激活邮件（FormSubmit 首次需激活）→ 确认邮件收到
5. Google Search Console 添加 yukfo.com + sitemap（可选，先提交首页收录）
6. 上线后检查清单：HTTPS 证书自动、移动端、5 页可达、表单通、页脚邮箱

- [ ] **Step 2: 提交**

```bash
cd "/d/YUKFO WED" && git add docs/DEPLOY.md && git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "docs: deploy guide for Cloudflare Pages"
```

---

## Self-Review 记录

- **Spec 覆盖**：5 页 ✓（Task 2-6）、视觉系统 ✓（Task 1）、素材方案 ✓（Task 7）、hero 变体 ✓（Task 9）、部署 ✓（Task 10）、风险项（邮箱可改=表单 action 集中一处 ✓、Logo 占位=Task 1 已用 logo.jpg ✓）
- **占位符**：无 TBD/TODO；Task 7 的 Unsplash ID 标注为"执行时获取"（真实 ID 无法预先写入计划，属可执行获取的信息，非占位）
- **类型一致性**：CSS 类名（.industry/.card/.form-grid/.notice）在 Task 2-6 的使用与 Task 1 定义一致；图片路径 `assets/images/industries/{kayak,outdoor,home,electronics}.jpg` 在 Task 4 引用与 Task 7 产出一致 ✓
