# yukfo.com 信任增强包 实施计划（v3.1）

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development。步骤使用 `- [ ]` 复选框跟踪。
> 背景：v3 文案优化完成后，用户以"游客视角"审阅全站，批准本包（对话内逐项确认，2026-08-14）：
> ① hero 深蓝成品感+数字信任条 ② 实体锚点（Yukfo Limited 香港 + 本人在长三角）三处落位 ③ 表单四件套（_next/_replyto/恢复 reCAPTCHA/_autoresponse）④ 新建 thanks.html。

**Goal:** 修掉游客视角的四个信任缺口：首屏半成品感、付定金"付给谁"、表单提交后脱品牌、无即时回执。

**Architecture:** 纯静态站改动：index.html + style.css（hero 深蓝）；about/faq/7 页页脚（实体锚点）；contact.html（表单四件套）；新建 thanks.html（noindex 转化页，不进 nav/sitemap）。校验器 PAGE_BAND 上界放宽（本包是有意新增信任元素，非压缩）。

**Tech Stack:** 静态 HTML/CSS；Python stdlib 校验器；git（`-c user.name="Jesus" -c user.email="hkyukfo@outlook.com"`）。

## Global Constraints（沿用 v3 铁律）

1. 不暗示自有工厂（统一 "partner factories"）
2. MOQ/交期零承诺；3. 不自嗨不绝对化；4. 客户地区统一 "clients overseas"（**例外：本包获用户批准披露自身实体位置**：Hong Kong / Yangtze River Delta）
5. 正文零破折号（title/meta 分隔符除外——注意：`_autoresponse` 的 value 在 body 内，也受此约束）
6. 无 AI 模板句；7. About 第三人称；8. 正文无 "we"
9. MUST_KEEP 事实清单不破坏（about 的 6/4/26/24h 等）
10. 提交身份 `git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit`，直接 master（用户批准）

---

### Task 1: hero 深蓝成品感 + 数字信任条 + 校验器带宽

**Files:** Modify: `assets/css/style.css`, `index.html`, `scripts/check_copy.py`

- [ ] **Step 1: CSS**。在 style.css 中，把现有 `.hero` 相关四行规则（`/* hero */` 注释块内的 `.hero{...}`、`.hero h1{...}`、`.hero p.sub{...}`、`.hero .accent{...}`）替换为：

```css
/* hero */
.hero{background:var(--blue);padding:72px 0 48px;border-bottom:1px solid var(--line)}
.hero h1{font-size:2.3rem;line-height:1.3;font-weight:700;max-width:760px;color:#fff}
.hero p.sub{font-size:1.12rem;color:rgba(255,255,255,.85);max-width:640px;margin:18px 0 30px}
.hero .accent{color:var(--gold)}
.hero .btn{background:var(--gold);border:1px solid var(--gold);color:#1a1a1a!important}
.hero .btn:hover{background:var(--gold-deep);color:#fff!important}
.hero .btn-ghost{background:transparent;color:#fff!important;border:1px solid rgba(255,255,255,.7)}
.hero .btn-ghost:hover{background:rgba(255,255,255,.12)}
.hero-stats{display:flex;gap:36px;margin-top:44px;flex-wrap:wrap}
.hero-stat .num{font-size:1.5rem;font-weight:700;color:var(--gold);line-height:1.2}
.hero-stat .lbl{font-size:.85rem;color:rgba(255,255,255,.75);margin-top:2px}
```
并在 `@media(max-width:760px)` 块内追加一行：`.hero-stats{gap:20px}`（现有移动端块内 `.hero h1{font-size:1.7rem}` 保留）。

- [ ] **Step 2: index.html hero 加数字条**。在 hero 容器内两个按钮之后、`</div>` 之前插入：

```html
      <div class="hero-stats">
        <div class="hero-stat"><div class="num">6</div><div class="lbl">years in cross-border trade</div></div>
        <div class="hero-stat"><div class="num">4</div><div class="lbl">markets served</div></div>
        <div class="hero-stat"><div class="num">26</div><div class="lbl">SKUs in one delivered program</div></div>
        <div class="hero-stat"><div class="num">24h</div><div class="lbl">reply time</div></div>
      </div>
```

- [ ] **Step 3: 校验器 PAGE_BAND 上界放宽**（本包有意新增信任元素，非压缩）。scripts/check_copy.py 中：
`PAGE_BAND = (0.70, 0.98)   # 单页压缩后词数 / 基线词数`
→
`PAGE_BAND = (0.70, 1.10)   # 上界放宽：v3.1 信任包（hero 数字条/实体锚点/表单隐藏字段）有意新增少量词`

- [ ] **Step 4: 校验 + 提交**
`python -X utf8 scripts/check_copy.py --page index` → 0 ERR（词数 ~106% 在带内）。
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add assets/css/style.css index.html scripts/check_copy.py
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: dark hero with trust stats strip, widen page word band"
```

---

### Task 2: 实体锚点三处 + 全站页脚

**Files:** Modify: `about.html`, `faq.html`, 7 页页脚（index/services/processes/deliveries/faq/about/contact.html）

- [ ] **Step 1: about.html**。"Service, Done the Right Way" 区块，stat-row 的 `</div>` 之后、区块 `</div>` 之前插入：

```html
      <p class="lead" style="margin-top:24px">Yukfo Limited is registered in Hong Kong. The work happens on the ground in the Yangtze River Delta.</p>
```

- [ ] **Step 2: faq.html**。付款条（Payment methods 答案）改为：

```html
<div class="faq-item"><h3>What payment methods do you accept?</h3><p>Bank transfer (T/T): 30% deposit to start production, 70% before shipment. Payments go to Yukfo Limited (Hong Kong). Sample costs are charged separately and deducted from your first production order. Repeat orders can negotiate different terms.</p></div>
```

- [ ] **Step 3: 7 页页脚**。把每个页脚的
`<span>© 2026 YUKFO. Custom manufacturing &amp; sourcing.</span>`
替换为
`<span>© 2026 YUKFO · Yukfo Limited, Hong Kong</span>`
（7 个文件各一处；thanks.html 尚未创建，不在此列）

- [ ] **Step 4: 校验 + 提交**
`python -X utf8 scripts/check_copy.py` → 除预期外 0 ERR（services/processes/deliveries/contact 之前已 PASS；index/about/faq 词数在放宽后的带内）。
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add about.html faq.html index.html services.html processes.html deliveries.html contact.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: entity anchor (Yukfo Limited, HK + Yangtze River Delta) on about/faq/footer"
```

---

### Task 3: 表单四件套 + thanks.html

**Files:** Modify: `contact.html`; Create: `thanks.html`

- [ ] **Step 1: contact.html 表单**。
  1. 删除 `<input type="hidden" name="_captcha" value="false">`（恢复 FormSubmit 默认 reCAPTCHA）
  2. 邮箱字段改名（FormSubmit `_replyto` 依赖名为 `email` 的字段）：`<input id="email" name="Email" type="email" required>` → `<input id="email" name="email" type="email" required>`（可见 label "Email *" 不动）
  3. 在 `_template` 行后新增两行（**注意 _autoresponse 的 value 正文零破折号铁律**）：
```html
        <input type="hidden" name="_next" value="https://yukfo.com/thanks">
        <input type="hidden" name="_autoresponse" value="Thanks for your inquiry. I'll reply within 24 hours on working days.">
```

- [ ] **Step 2: 新建 thanks.html**（完整文件，直接创建）：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Message Received — YUKFO</title>
<meta name="robots" content="noindex">
<meta property="og:title" content="Message Received — YUKFO">
<meta property="og:type" content="website">
<link rel="icon" type="image/jpeg" href="assets/images/logo.jpg">
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
      <a href="processes">Processes</a>
      <a href="deliveries">Deliveries</a>
      <a href="faq">FAQ</a>
      <a href="about">About</a>
      <a href="contact">Contact</a>
    </nav>
    <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
  </div>
</header>

<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Message Received</h2>
      <p class="lead">Your inquiry is in. I reply within 24 hours on working days.</p>
      <div class="qstep"><div class="num">1</div><div><h3>I Check the Details</h3><p>Your drawing, specs, and target price go against real factory data.</p></div></div>
      <div class="qstep"><div class="num">2</div><div><h3>You Get My Reply</h3><p>Questions, options, or a quote path, within 24 hours on working days.</p></div></div>
      <div class="qstep"><div class="num">3</div><div><h3>Samples First, Then Production</h3><p>You approve samples before mass production starts. Nothing moves without your confirmation.</p></div></div>
      <p class="lead" style="margin-top:24px">Faster? WhatsApp <a href="https://wa.me/8617860570306">+86 178 6057 0306</a> or email <a href="mailto:hkyukfo@outlook.com">hkyukfo@outlook.com</a>.</p>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container footer-inner">
    <span>© 2026 YUKFO · Yukfo Limited, Hong Kong</span>
    <span><a href="mailto:hkyukfo@outlook.com">hkyukfo@outlook.com</a></span>
  </div>
</footer>
</body>
</html>
```
（不入 sitemap.xml、不加入任何页面导航列表——本页自身复用标准 header nav 是允许的）

- [ ] **Step 3: 校验 + 提交**
`python -X utf8 scripts/check_copy.py --page contact thanks` → contact 0 ERR（词数 ~110% 在放宽后带内）；thanks 0 ERR（无基线，打印"无基线，跳过带检查"属预期）。
本地验证 /thanks 路由：`curl -s -o /dev/null -w "%{http_code}" http://localhost:8931/thanks` → 200（预览服务器已带 clean-URL 回退）。
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add contact.html thanks.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: form upgrade (next/replyto/captcha/autoresponse) + thanks page"
```

---

### Task 4: 同步 public/ 并全站终验

**Files:** Modify: `public/*.html`（复制）

- [ ] **Step 1: 同步**
```bash
cd "/d/YUKFO WED"
cp index.html services.html processes.html deliveries.html faq.html about.html contact.html thanks.html sitemap.xml public/
cp assets/css/style.css public/assets/css/style.css
```
- [ ] **Step 2: 终验**
`python -X utf8 scripts/check_copy.py` → 8 页全部 PASS 0 错误（thanks 无基线跳过带检查属预期）；`diff -rq --exclude=.git . public/` 仅 "Only in" 行无 "Files ... differ"。
- [ ] **Step 3: 提交**
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add -A
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: sync public/ with trust pack"
```
- [ ] **Step 4: 提醒用户**：① 拖 public/ 上传 Cloudflare ② **部署后必须实测表单**：提交一次真实询盘，确认收到邮件 + reCAPTCHA 正常 + 提交后跳转 /thanks + 提交邮箱收到 autoresponse（若 autoresponse 没到，检查 FormSubmit 配置）。

---

## Self-Review（写计划时已跑）

1. **Spec 覆盖**：四个获准项全部有对应任务（hero→T1，锚点→T2，表单→T3，thanks→T3）；校验器兼容性（新增页无基线、词数带）已处理。✅
2. **占位符扫描**：无 TBD；所有代码/文案完整给出。✅
3. **一致性**：`_autoresponse` value 无破折号（铁律 5 覆盖 body 内文本）；页脚新文案 7 页一致；thanks.html 沿用标准 header/footer；PAGE_BAND 1.10 覆盖 index ~106% 与 contact ~110%。✅
4. **已知取舍（记录在案）**：`_replyto` 依赖字段名 `email`（FormSubmit 文档模式）→ 字段 name 改名，部署后实测确认；reCAPTCHA 恢复后中国内地访客可能加载不出验证码（受众为海外买家，接受）；hero 金色按钮对比度已按 WCAG 验证（#1a1a1a on #ffc107 ≈ 9:1）。✅
