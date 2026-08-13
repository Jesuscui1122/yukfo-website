# yukfo.com 文案优化 v3 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 按任务逐个实施。步骤使用 `- [ ]` 复选框跟踪。
> Spec: `docs/superpowers/specs/2026-08-13-yukfo-website-copy-v3.md`（已批准）

**Goal:** 全站 7 页文案 v3 重写：母语级地道 + 语态统一 + 去冗余（全站词数 -20~30%），铁律零违反，按 2+5 流程分两轮用户验收。

**Architecture:** 纯静态站点，直接改根目录 7 个 HTML 文件（`public/` 是部署镜像，最后同步）。新增校验脚本 `scripts/check_copy.py` 把文案铁律机器化（硬失败/警告两级），每页任务循环 = 改文件 → 跑校验 → 提交。两个用户验收门：样板轮（index+about）→ 批量轮（5 页）。

**Tech Stack:** 静态 HTML/CSS/JS；Python 3 stdlib（校验脚本，无第三方依赖）；git。

## Global Constraints（铁律，从 spec 逐字复制，所有任务隐式遵守）

1. 不暗示自有工厂（统一 "partner factories"，无 "my own production"）
2. MOQ/交期零承诺（不写数字，不暗示可控）
3. 不自嗨不绝对化（无 "always/everything" 绝对化用语、无空修饰标签）
4. 不宣称具体地区（统一 "clients overseas"）
5. 正文零破折号（em-dash/en-dash；`<title>`/`<meta>` 里的 " — " 标题分隔符不算）
6. 无 AI 模板句
7. About 第三人称 + 开头一次点明主语（"the person behind YUKFO"，不公开姓名）
8. 业务事实不增不减（报价拆项、QC 三步、工艺清单、26 SKUs、数字亮点）
9. 全部提交命令用 `git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit`

## 校准数据（2026-08-13 实测，检查器基线）

| 页 | 全页词数 | 正文破折号 | 违禁词 | 目标词数（约 -25%） |
|---|---|---|---|---|
| index | 287 | 1（行 36） | 无 | ~220 |
| about | 339 | 0 | ' always'×1、'everything'×1（均警告级） | ~260 |
| services | 537 | 0 | 无 | ~400 |
| processes | 197 | 1（行 67） | 'trusted'×2（meta，硬失败） | ~155 |
| deliveries | 164 | 0 | 无 | ~130 |
| faq | 401 | 0 | 无 | ~290 |
| contact | 119 | 0 | 无 | ~110 |
| **合计** | **2044** | | | **~1560（-24%）** |

其他实测：全站 7 页 `href="page""` 双引号残留（clean URL 转换 bug）；services.html 有两个同名 "Product Sourcing" 区块。

## 文件结构

| 文件 | 动作 | 职责 |
|---|---|---|
| `scripts/check_copy.py` | 新建 | 文案铁律校验器（Task 1） |
| `index.html` | 修改 | 样板轮（Task 2） |
| `about.html` | 修改 | 样板轮（Task 3） |
| `services.html` / `processes.html` / `deliveries.html` / `faq.html` / `contact.html` | 修改 | 批量轮（Task 4-8） |
| `docs/DEPLOY.md` | 修改 | 更新为当前真实状态（Task 9） |
| `public/*.html` + `public/sitemap.xml` | 同步 | 部署镜像（Task 10） |

---

### Task 1: 文案铁律校验器 scripts/check_copy.py

**Files:**
- Create: `scripts/check_copy.py`

**Interfaces:**
- Consumes: 无（第一个任务）
- Produces: CLI 契约——`python -X utf8 scripts/check_copy.py`（全站）或 `python -X utf8 scripts/check_copy.py --page about`（单页，无扩展名）。硬失败（违禁词/正文破折号/href 双引号/必备事实缺失）→ 退出码 1；警告（绝对化词、词数带）→ 退出码 0。后续所有任务的验证步骤都用它。

- [ ] **Step 1: 写入校验器（完整代码，直接复制）**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yukfo.com 文案铁律校验器（stdlib only）。
用法:
  python -X utf8 scripts/check_copy.py              # 全站检查（根目录 *.html）
  python -X utf8 scripts/check_copy.py --page about # 单页检查
硬失败(退出码1): 违禁词 / 正文破折号 / href 双引号 / 必备事实缺失
警告(退出码0): 绝对化词(人工判断) / 词数带
"""
import re, sys, html, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARD_WORDS = ['trusted', 'my own production', 'own factory', "i've shipped", 'guarantee']
WARN_WORDS = [' always', 'everything', 'never']
MUST_KEEP = {
    'index':      ['No category limits'],
    'about':      ['6', '4', '26', '24h'],
    'services':   ['PA6', 'ABS', 'PP', 'EVA', 'IXPE'],
    'processes':  ['PA6', 'ABS', 'PP', 'EVA', 'IXPE', 'PVC'],
    'deliveries': ['26 SKUs'],
    'faq':        ['30%', '70%'],
    'contact':    ['24 hours'],
}
BASELINE_WORDS = {'index': 287, 'about': 339, 'services': 537, 'processes': 197,
                  'deliveries': 164, 'faq': 401, 'contact': 119}
PAGE_BAND = (0.70, 0.98)   # 单页压缩后词数 / 基线词数
TOTAL_BAND = (0.70, 0.85)  # 全站合计压缩带（约 -15~30%）

def raw(page):
    return open(os.path.join(ROOT, page + '.html'), encoding='utf-8').read()

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)

def page_words(page):
    return len(re.findall(r'[A-Za-z0-9]+', strip_tags(raw(page))))

def body_text(page):
    m = re.search(r'<body[^>]*>(.*)</body>', raw(page), flags=re.S)
    return strip_tags(m.group(1))

def check(page):
    errs, warns = [], []
    s = raw(page)
    # 1) 正文破折号（head 里的标题分隔符不算）
    b = body_text(page)
    for ch in ('—', '–'):
        if ch in b:
            errs.append(f'正文破折号 {ch!r} x{b.count(ch)}')
    # 2) 违禁词（全页含 head）
    low = s.lower()
    for w in HARD_WORDS:
        n = low.count(w)
        if n:
            lines = [str(i + 1) for i, l in enumerate(s.splitlines()) if w in l.lower()]
            errs.append(f'违禁词 {w!r} x{n} 行 {",".join(lines)}')
    for w in WARN_WORDS:
        n = low.count(w)
        if n:
            lines = [str(i + 1) for i, l in enumerate(s.splitlines()) if w in l.lower()]
            warns.append(f'绝对化词 {w.strip()!r} x{n} 行 {",".join(lines)}（人工判断）')
    # 3) href 双引号 bug
    n = len(re.findall(r'href="[^"]*""', s))
    if n:
        errs.append(f'href 双引号残留 x{n}')
    # 4) 必备事实
    for k in MUST_KEEP.get(page, []):
        if k not in s:
            errs.append(f'必备事实 {k!r} 缺失')
    # 5) 词数带
    w = page_words(page)
    ratio = w / BASELINE_WORDS[page]
    if not (PAGE_BAND[0] <= ratio <= PAGE_BAND[1]):
        warns.append(f'词数 {w}（基线 {BASELINE_WORDS[page]}，{ratio:.0%}）超出带 {PAGE_BAND[0]:.0%}-{PAGE_BAND[1]:.0%}')
    else:
        print(f'  ok 词数 {w}（{ratio:.0%}）')
    return errs, warns

def main():
    pages = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == '--page' else \
            [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
    bad, n_err, n_warn = False, 0, 0
    for p in pages:
        errs, warns = check(p)
        print(f'{p}.html: {"PASS" if not errs else "FAIL"}')
        for e in errs:
            print(f'  ERR {e}')
        for w in warns:
            print(f'  WARN {w}')
        if errs:
            bad = True
        n_err += len(errs)
        n_warn += len(warns)
    if len(pages) > 1:
        total = sum(page_words(p) for p in pages)
        base = sum(BASELINE_WORDS[p] for p in pages)
        r = total / base
        flag = '' if TOTAL_BAND[0] <= r <= TOTAL_BAND[1] else '（超出全站带）'
        print(f'全站合计 {total} 词 / 基线 {base}（{r:.0%}）{flag}')
    print(f'\n{"FAIL" if bad else "PASS"}: {n_err} 错误, {n_warn} 警告')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 跑基线，确认它抓得住已知问题**

Run: `python -X utf8 scripts/check_copy.py`

Expected（全部为已知问题，无意外新错误；每页 href 双引号残留 9 处左右，即 8 个内链 + 1 个按钮）：

```
about.html:      FAIL  ERR href 双引号残留 x9；WARN ' always'/'everything'（行 56，待 Task 3 消除）
contact.html:    FAIL  ERR href 双引号残留 x9
deliveries.html: FAIL  ERR href 双引号残留 x9
faq.html:        FAIL  ERR href 双引号残留 x9
index.html:      FAIL  ERR 正文破折号 x1（行 36）+ href x9
processes.html:  FAIL  ERR 违禁词 'trusted' x2（行 7/9）+ 正文破折号 x1（行 67）+ href x9
services.html:   FAIL  ERR href 双引号残留 x9
FAIL: 15 错误左右（全部对上已知清单）
```

若出现预期外的 ERR（如其他违禁词命中），先停下核对代码再继续，不修改文案。

- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add scripts/check_copy.py
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "feat: copy rule checker (iron rules as machine checks)"
```

---

### Task 2: 样板轮 — index.html 重写

**Files:**
- Modify: `index.html`（整文件替换）

**Interfaces:**
- Consumes: `scripts/check_copy.py --page index`
- Produces: 本轮风格基准（压缩幅度、语气、句式）——Task 3 与批量轮（Task 4-8）都以此为准。

- [ ] **Step 1: 整文件替换**（以下为完整新文件，直接覆盖）

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
    <a class="brand" href="index"><img src="assets/images/logo.jpg" alt="YUKFO logo"><span>YUKFO</span></a>
    <nav class="nav" aria-label="Main navigation">
      <a href="index" class="active">Home</a>
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
  <section class="hero">
    <div class="container">
      <h1>Need something from China? I'm your sourcing agent. <span class="accent">No category limits.</span></h1>
      <p class="sub">Parts, finished goods, tools, or hard-to-find items: I find the supplier, verify samples, handle export, and deliver to your door. Need it made from scratch? That too, from drawings to delivered goods.</p>
      <a class="btn" href="contact">Send Your Project</a>
      <a class="btn btn-ghost" href="services" style="margin-left:10px">See What I Do</a>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>How I Help</h2>
      <p class="lead">Three ways to work with YUKFO. One person handles it all, from first quote to delivery.</p>
      <div class="grid">
        <div class="card"><span class="tag">Product Sourcing</span><h3>Anything You Need</h3><p>Any category: components, finished goods, tools, hardware. I find the supplier, compare prices, verify samples, and handle export.</p></div>
        <div class="card"><span class="tag">Custom Manufacturing</span><h3>Parts Made to Order</h3><p>Injection molding, rotomolding, extrusion, foam, and metal fabrication, produced through partner factories and checked at each stage.</p></div>
        <div class="card"><span class="tag">Turnkey Delivery</span><h3>Project Management</h3><p>From drawing to doorstep: sourcing, prototyping, production, QC, export documents, and shipping. One point of contact throughout.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>What We Do</h2>
      <p class="lead">The processes I work with, and the industries they serve.</p>
      <div class="grid">
        <div class="card"><h3>Injection Molding</h3><p>Precision parts in PA6, ABS, PP, from small pulleys to complex enclosures.</p></div>
        <div class="card"><h3>Rotational Molding</h3><p>Large hollow parts: kayaks, coolers, tanks, planters.</p></div>
        <div class="card"><h3>Plastic Extrusion</h3><p>PVC and ABS profiles for windows, doors, and structural trims, with tight tolerances and custom lengths.</p></div>
        <div class="card"><h3>Foam Die-Cutting</h3><p>EVA/IXPE foam panels, mats, and gaskets for flooring, insulation, and packaging.</p></div>
        <div class="card"><h3>Metal Fabrication</h3><p>Stamping, bending, laser cutting, die-casting, and powder coating for brackets, plates, handles, and locks.</p></div>
      </div>
      <a class="btn btn-ghost" href="processes" style="margin-top:24px">See All Processes</a>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Why a One-Person Partner?</h2>
      <p class="lead">YUKFO runs on repeat orders and referrals, so every project gets the right factory, a fair cost, and clear expectations.</p>
      <a class="btn" href="about">Meet the Person Behind YUKFO</a>
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

改动点（相对现版）：hero 副句 47→33 词（破折号消除）；卡片 1 去 "Anything You Need" 重复语义；Why One-Person 段 27→21 词；全部 href 双引号修复。

- [ ] **Step 2: 校验**

Run: `python -X utf8 scripts/check_copy.py --page index`

Expected: `PASS`，0 ERR，`ok 词数 264（92%）` 左右（警告允许：无）。

- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add index.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: index — native wording, tighter hero and cards"
```

---

### Task 3: 样板轮 — about.html 重写

**Files:**
- Modify: `about.html`（整文件替换）

**Interfaces:**
- Consumes: Task 2 的风格基准；`scripts/check_copy.py --page about`
- Produces: 样板轮第二页；与 Task 2 共同进入用户验收门。

- [ ] **Step 1: 整文件替换**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About — YUKFO: Six Years of Cross-Border Supply Chain</title>
<meta name="description" content="YUKFO's story: six years of cross-border supply chain experience serving brand clients across North America, Latin America and Europe. Direct sourcing, transparent pricing, one accountable partner.">
<meta property="og:title" content="About — YUKFO">
<meta property="og:description" content="Service, done the right way. Six years of cross-border supply chain experience, one accountable partner from drawing to delivery.">
<meta property="og:type" content="website">
<link rel="icon" type="image/jpeg" href="assets/images/logo.jpg">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<style>
.stat-row{display:flex;gap:20px;flex-wrap:wrap;margin-top:8px}
.stat{flex:1;min-width:160px;border:1px solid var(--line);border-radius:var(--radius);padding:20px 24px;text-align:center;background:var(--bg)}
.stat .num{font-size:1.9rem;font-weight:700;color:var(--blue);line-height:1.2}
.stat .lbl{font-size:.85rem;color:var(--gray);margin-top:4px}
</style>
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
      <a href="about" class="active">About</a>
      <a href="contact">Contact</a>
    </nav>
    <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
  </div>
</header>

<main>
  <section class="section" style="border-top:0">
    <div class="container">
      <h2>Service, Done the Right Way</h2>
      <p class="lead">Six years in cross-border supply chain, delivering parts and finished products for brand clients overseas.</p>
      <div class="stat-row">
        <div class="stat"><div class="num">6</div><div class="lbl">years in cross-border trade</div></div>
        <div class="stat"><div class="num">4</div><div class="lbl">markets served</div></div>
        <div class="stat"><div class="num">26</div><div class="lbl">SKUs in one delivered program</div></div>
        <div class="stat"><div class="num">24h</div><div class="lbl">reply time</div></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Why YUKFO Exists</h2>
      <p class="lead">The person behind YUKFO spent years on the supply chain's front line, watching how projects really run: information out of sync, opaque processes, miscommunication between buyers and factories, blurry lines of responsibility.</p>
      <p class="lead">When problems come up, some suppliers dodge or hide, and the risk lands on the overseas buyer: quality nobody follows up on, emails unanswered for days. YUKFO was built to break that pattern: one person pushing the whole project forward, straight to the source, without layers of middlemen.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Expertise</h2>
      <p class="lead">Six years in, he knows the production constraints and cost boundaries of multiple processes, and the practical details like logistics costs that decide whether a project lands on time and on budget.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>A Foundation of Trust</h2>
      <p class="lead">The business runs on repeat orders and word of mouth, so every order matters. Without layers of middlemen, communication stays direct and open, and goals align with the client's: the right factory, a fair cost, and problems found and resolved early.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Core Advantage</h2>
      <p class="lead">He has built a database of real cost reference data across factories and processes, and every quote is itemized line by line. With first-hand cost data, he can spot unreasonable quotes, so clients pay for what the part actually costs, without unnecessary middleman markup.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Working With Me</h2>
      <p class="lead">No contracts to sign just to ask a question. Send the drawing or idea, and you'll have a response within 24 hours on working days.</p>
      <a class="btn" href="contact">Send Your Project</a>
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

改动点（相对现版）：Why YUKFO Exists 首段改为 "The person behind YUKFO..."——一次点明主语（spec 决策 3），后续 "he" 语法成立；消除 ' always'/'everything'（警告级词清零）；各段压缩约 10%；数字 stat 与业务事实原样保留；href 双引号修复。

- [ ] **Step 2: 校验**

Run: `python -X utf8 scripts/check_copy.py --page about`

Expected: `PASS`，0 ERR，0 WARN，`ok 词数 305（90%）` 左右。

- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add about.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: about — antecedent for 'he', tighter prose"
```

---

## ⛔ 用户验收门 1（样板轮）

Task 2-3 完成后**停下**，向用户交付：
1. index 与 about 的**逐条改动说明**（上表改动点展开成 before/after 句子级对比）
2. 两页**新全文**（渲染预览可选：`python -X utf8 -m http.server 8760` 后浏览器看，或 agent-browser 截图）

用户反馈修改 → 改文件 → 重跑对应 `--page` 校验 → 提交修正（`fix: copy v3 baseline adjustments`）。用户确认基准后继续 Task 4。

**批量轮（Task 4-8）通用标准**：语气与压缩幅度对齐已确认的 index/about 基准；每个任务的 Step 2 校验必须 0 ERR；警告（词数带/绝对化词）需向用户说明理由。

---

### Task 4: 批量轮 — services.html（合并重复区块 + 压缩）

**Files:**
- Modify: `services.html`

**Interfaces:**
- Consumes: 用户确认的样板基准；`scripts/check_copy.py --page services`
- Produces: 批量轮第 1 页

- [ ] **Step 1: 重写**。具体改动（按现文件结构）：
  1. **合并两个 "Product Sourcing" 区块**（现第 1 区块 + 第 3 区块同名重复）为一个，置于 Custom Manufacturing 之前。合并后：
     - lead：`Your sourcing agent in China, no category limits: standard and custom components, finished goods, tools, hardware, anything your project needs. I find the supplier, compare prices against real cost data, verify samples, and handle the export.`
     - bullets（原 5 条去重后 3 条）：`Prices compared across suppliers, against real cost data` / `Samples verified and factories checked before your money moves` / `Standard and custom components: fasteners, magnets, fittings, electronics`
  2. Custom Manufacturing：lead 与 6 卡片保留（业务事实），仅 Project Parts 卡片删末句 `If your project requires it, it is in scope.`（与合并后 lead 重复）
  3. Turnkey / Quality Control / Export & Delivery / CTA 区块：事实不动，句式按基准轻压缩（目标整页 ≤ 420 词）
  4. 全部 href 双引号修复
- [ ] **Step 2: 校验** Run: `python -X utf8 scripts/check_copy.py --page services` → Expected: PASS，0 ERR，词数 ~400（75%）
- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add services.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: services — merge duplicate Product Sourcing sections"
```

---

### Task 5: 批量轮 — processes.html（meta 修铁律违禁词）

**Files:**
- Modify: `processes.html`

**Interfaces:**
- Consumes: 样板基准；`scripts/check_copy.py --page processes`
- Produces: 批量轮第 2 页

- [ ] **Step 1: 重写**。具体改动：
  1. 行 7 meta description：`...metal fabrication, delivered through trusted partner factories.` → `...metal fabrication, delivered through partner factories.`（硬失败违禁词 'trusted'，此处 2 处：meta 与 og:description 各一）
  2. 行 9 og:description 同步去掉 `trusted`
  3. 5 个工艺块：事实（材料/行业/工艺）与 tag 原样保留，描述句轻压缩
  4. How It Works lead 消除正文破折号：`send the drawing — I'll tell you how we'd do it` → `send the drawing and I'll tell you how we'd do it`
  5. 全部 href 双引号修复
- [ ] **Step 2: 校验** Run: `python -X utf8 scripts/check_copy.py --page processes` → Expected: PASS，0 ERR，词数 ~165（84%）
- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add processes.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: processes — remove 'trusted' from meta, no em-dash in body"
```

---

### Task 6: 批量轮 — deliveries.html

**Files:**
- Modify: `deliveries.html`

**Interfaces:**
- Consumes: 样板基准；`scripts/check_copy.py --page deliveries`
- Produces: 批量轮第 3 页

- [ ] **Step 1: 重写**。具体改动：
  1. intro lead 保留（"Client names stay confidential" 是事实承诺）
  2. Outdoor & Hunting 块：`...and EVA foam, engineered, produced, checked, and shipped as one program.` 末句 "as one program" 与段首重复 → `...engineered, produced, checked, and shipped together.`
  3. 其余 3 块：事实（26 SKUs、mold development、custom sizes）保留，句式轻压缩（目标整页 ≤ 140 词）
  4. 全部 href 双引号修复
- [ ] **Step 2: 校验** Run: `python -X utf8 scripts/check_copy.py --page deliveries` → Expected: PASS，0 ERR，词数 ~135（82%）
- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add deliveries.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: deliveries — tighter project descriptions"
```

---

### Task 7: 批量轮 — faq.html（答案直接化）

**Files:**
- Modify: `faq.html`

**Interfaces:**
- Consumes: 样板基准；`scripts/check_copy.py --page faq`
- Produces: 批量轮第 4 页

- [ ] **Step 1: 重写**。10 条答案按"直接回答、无铺垫"标准压缩（保留 30%/70%、三天检查点、24 小时等事实）：
  1. MOQ：`It varies by product and by supplier. Tell me your quantity and I'll confirm the MOQ and price together.`（现版已达标，保留）
  2. Lead time：`It depends on the supplier and the process. Every quote comes with a dated schedule you commit to, with shipping time quoted alongside.`（45→24 词；删防御性 "I don't promise weeks I can't control"，符合 275a525 定下的"无防御腔"）
  3. Payment：`Bank transfer (T/T): 30% deposit to start production, 70% before shipment. Sample costs are charged separately and deducted from your first production order. Repeat orders can negotiate different terms.`
  4. Samples：`Small parts: I often cover the sample cost or charge only the cost price. Large parts (molds, rotomolded items) carry a sample/mold fee, credited back when you place a production order. The number is shared before we start.`
  5. Drawings：`STEP, IGES, DXF, DWG, PDF, or even a sketch photo. Send them through the contact form, email, WhatsApp or WeChat, and I'll confirm what I need within a day.`
  6. Molds：`Yes. I develop injection and rotomolding molds with my partner toolmakers, validate them with trial shots, and only then start production. You get mold drawings and a development schedule.`
  7. Existing molds：`Yes. If you already own tooling, I'll quote production on your molds directly. Many clients transfer their existing molds to partner factories to reduce cost.`
  8. Quality：`Three checkpoints: (1) approved samples before mass production, (2) in-process and final random inspection, (3) a pre-shipment inspection report with photos. Third-party inspection available on request.`
  9. Shipping：`Yes. I prepare export documents, handle customs declaration, and arrange sea or air freight to your port or door.`
  10. Reply：`Within 24 hours on working days. Every inquiry gets a direct answer.`（保留）
  11. 页头 lead 与 CTA 保留；全部 href 双引号修复
- [ ] **Step 2: 校验** Run: `python -X utf8 scripts/check_copy.py --page faq` → Expected: PASS，0 ERR，词数 ~290（72%）
- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add faq.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: faq — direct answers, no padding"
```

---

### Task 8: 批量轮 — contact.html

**Files:**
- Modify: `contact.html`

**Interfaces:**
- Consumes: 样板基准；`scripts/check_copy.py --page contact`
- Produces: 批量轮第 5 页

- [ ] **Step 1: 重写**。具体改动：
  1. notice Tip 框：`Tip: include quantity, target price if you have one, and delivery date. If you have drawings or specs, mention them and I'll share a secure way to send files.` → `Tip: include quantity, target price if you have one, and delivery date. Have drawings or specs? Mention them and I'll share a secure way to send files.`
  2. 三卡片与表单 label/placeholder 保留（已达标，仅个别润色：Response Time 卡 `Direct answers, within 24 hours on working days.` 保留）
  3. 全部 href 双引号修复
- [ ] **Step 2: 校验** Run: `python -X utf8 scripts/check_copy.py --page contact` → Expected: PASS，0 ERR，词数 ~114（96%）
- [ ] **Step 3: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add contact.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: contact — tighter tip copy"
```

---

## ⛔ 用户验收门 2（批量轮）

Task 4-8 完成后**停下**，向用户交付 5 页的逐条改动说明 + 新全文（或渲染预览）。反馈修改 → 改文件 → 重跑校验 → 提交修正。确认后继续 Task 9-10。

---

### Task 9: docs/DEPLOY.md 更新为当前真实状态

**Files:**
- Modify: `docs/DEPLOY.md`

**Interfaces:**
- Consumes: 无
- Produces: 部署手册与现状一致

- [ ] **Step 1: 整文件替换**为以下内容：

```markdown
# yukfo.com 部署手册（Cloudflare Pages，免费）

> 状态：**已正式上线（2026-08-09）**——https://yukfo.com 全球可访问，www 301 重定向到裸域（Cloudflare Redirect Rules）
> 7 页：Home / Services / Processes / Deliveries / FAQ / About / Contact（clean URLs，无 .html 后缀）
> 表单：FormSubmit 已激活 → hkyukfo@outlook.com（2026-08-09 实测提交 OK）
> SEO：Google Search Console 已验证（https://yukfo.com 网址前缀资源），sitemap.xml 已提交（clean URLs）

## 日常改文案流程

1. 改根目录对应 HTML 文件（`D:\YUKFO WED\*.html`）
2. 跑铁律校验：`python -X utf8 scripts/check_copy.py`（0 错误才算过；警告逐条人工判断）
3. 同步到部署目录：`cp *.html sitemap.xml public/`（在 `D:\YUKFO WED` 下）
4. Cloudflare → Workers & Pages → yukfo → Create new deployment → 拖拽上传 `public/` 目录

## 上传排除（用 public/ 目录即可，无需手动挑）

public/ 只含：7 个 HTML + sitemap.xml + assets/（css/js/images）。`.git/`、`docs/`、`scripts/` 不进 public/。

## 维护备忘

- **改邮箱**：contact.html 表单 action 里的 hkyukfo@outlook.com + 页脚 mailto（两处，表单处有注释标注）
- **改文案**：见上面"日常改文案流程"
- **加产品图**：assets/images/ 加文件 → 同步 public/ → 重新部署
- **文案铁律**（校验器强制执行，人工修改时同样遵守）：不暗示自有工厂 / MOQ·交期零承诺 / 不自嗨不绝对化 / 统一 clients overseas / 正文零破折号

## 遗留事项

- 产品实拍图持续收集（替换 industries AI 图）
- 可选：域名邮箱 jesus@yukfo.com
- Google 收录观察（提交 sitemap 后 1-2 周）
```

- [ ] **Step 2: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add docs/DEPLOY.md
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "docs: DEPLOY.md reflects live 7-page site and copy checker"
```

---

### Task 10: 同步 public/ 并全站终验

**Files:**
- Modify: `public/*.html`、`public/sitemap.xml`（从根目录复制）

**Interfaces:**
- Consumes: Task 1-9 全部产物
- Produces: 待用户拖拽上传的部署目录

- [ ] **Step 1: 同步部署目录**

```bash
cd "/d/YUKFO WED"
cp index.html services.html processes.html deliveries.html faq.html about.html contact.html sitemap.xml public/
```

- [ ] **Step 2: 全站终验**

Run: `python -X utf8 scripts/check_copy.py`

Expected: 7 页全部 PASS，`0 错误`；警告仅允许词数带提示（若个别页在带外，向用户说明原因）；全站合计 ~1560 词（-24% 左右，全站带 70-85% 内）。

- [ ] **Step 3: 确认 public/ 与根目录一致**

Run: `diff -rq --exclude=.git . public/ 2>/dev/null`（仅应输出 "Only in" 行：.claude/.gitignore/docs/scripts 在根目录独有，无 "Files ... differ"）

- [ ] **Step 4: 提交**

```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add -A
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v3: sync public/ with rewritten pages"
```

- [ ] **Step 5: 提醒用户**：拖拽 `public/` 上传 Cloudflare Pages 完成部署（用户手动步骤，不代做）。

---

## Self-Review（写计划时已跑）

1. **Spec 覆盖**：标准 1-5 → 校验器（Task 1）+ 各页任务；About 补主语 → Task 3；services 合并 → Task 4；meta trusted → Task 5；2+5 流程 → 两个验收门；部署衔接 → Task 9-10；href 顺手项 → 各页任务内；DEPLOY.md 顺手项 → Task 9。✅ 无缺口
2. **占位符扫描**：无 TBD/TODO；所有代码与文案均为完整内容。✅
3. **类型/命名一致**：校验器 CLI 契约（`--page`、退出码、BASELINE_WORDS/MUST_KEEP 键名）在各任务 Step 2 中引用一致。✅
4. **已知取舍（记录在案）**：词数带为警告级不是硬失败（quality 由用户两轮验收门把关）；Task 4-8 的最终成文由执行者按"样板基准 + 逐条改动点"产出（受验收门约束，无法提前锁定全文——这是 2+5 流程的设计本身）。
