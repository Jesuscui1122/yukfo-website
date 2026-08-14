# yukfo.com 交易者声音 v4 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development。步骤使用 `- [ ]` 复选框跟踪。
> 背景：用户对 v3 文案的评价"太大众化，大多数网站都这样说"。经四套声音样片对比，用户选定 **B 交易者**（"You send X. I do Y."）。本计划把全站仍"大众化"的句子换成交易者声音——**只换句子，不加新内容**（用户已否决证据区方案）。

**Goal:** 全站文案换成交易者声音：You/I 对子、动作为主、钱的位置说清楚、短句。铁律不变。

**Architecture:** 精确 old→new 句子替换（18 处，覆盖 6 页；contact.html 已在目标声音内，零改动）。每处替换都是现存句的改写，不加新事实、不加新区块。

**Tech Stack:** 静态 HTML；校验器 scripts/check_copy.py；git（`-c user.name="Jesus" -c user.email="hkyukfo@outlook.com"`，直接 master）。

## Global Constraints（铁律，全不变）

1. 不暗示自有工厂（"partner factories" 保留）
2. MOQ/交期零承诺；3. 不绝对化（无 always/everything/never）；4. clients overseas
5. 正文零破折号；6. 无 AI 模板句；7. About 第三人称（"The person behind YUKFO" 保留）；8. 正文无 "we"
9. MUST_KEEP 事实（PA6/ABS/PP/EVA/IXPE/PVC、26 SKUs、30%/70%、6/4/26/24h、'24 hours'）全部不动
10. 只做本计划列出的 old→new 替换，**任何句子不在替换清单里就一个字都不许动**（含 meta/title/按钮/页脚/hero/stats/thanks.html）

## 声音规则（替换句必须符合）

1. You/I 对子：客户动作 + 我的动作
2. 动作为主：删修饰词（experienced 等），只留动作和对象
3. 钱的位置："samples checked before your money moves"、"production starts after you approve" 这类既存事实可直说，不吆喝
4. 短句，一句一个动作

---

### Task 1: index.html + services.html

**Files:** Modify: `index.html`, `services.html`

**Interfaces:** Consumes 无；Produces 交易者声音基准（Task V4-2 参考）。

- [ ] **Step 1: 应用以下精确替换**（每个 old 串在文件中必须恰好出现一次；若找不到或出现多次，STOP 报 NEEDS_CONTEXT，不许猜）

index.html：

1. `Parts, finished goods, tools, or hard-to-find items: I find the supplier, verify samples, handle export, and deliver to your door. Need it made from scratch? That too, from drawings to delivered goods.`
→ `Parts, finished goods, tools, or hard-to-find items: I find the factory, check the samples, handle export, and deliver to your door. Need it made from scratch? You send drawings. I deliver goods.`

2. `Three ways to work with YUKFO. One person handles it all, from first quote to delivery.`
→ `Three ways to work with me. You send the drawing or the idea. I do the rest.`

3. `Any category: components, finished goods, tools, hardware. I find the supplier, compare prices, verify samples, and handle export.`
→ `You need it, I find it: parts, finished goods, tools, hardware. Factories compared, samples checked before your money moves, export handled.`

4. `Injection molding, rotomolding, extrusion, foam, and metal fabrication, produced through partner factories and checked at each stage.`
→ `Injection molding, rotomolding, extrusion, foam, metal. Made in partner factories. Samples approved before production.`

5. `From drawing to doorstep: sourcing, prototyping, production, QC, export documents, and shipping. One point of contact throughout.`
→ `You send a drawing. I handle sourcing, prototyping, production, QC, documents, shipping. One contact: me.`

6. `The processes I work with, and the industries they serve.`
→ `Five processes I work with, and the industries they serve.`

7. `YUKFO runs on repeat orders and referrals, so every project gets the right factory, a fair cost, and clear expectations.`
→ `I live on repeat orders and referrals. That means the right factory, a fair cost, and clear expectations on every order.`

services.html：

8. `Your sourcing agent in China, no category limits: standard and custom components, finished goods, tools, hardware, anything your project needs. I find the supplier, compare prices against real cost data, verify samples, and handle the export.`
→ `You name it, I source it: standard or custom components, finished goods, tools, hardware. Prices compared against real cost data, samples verified, export handled.`

9. `When your project needs a part made from scratch, I can make it too, through partner factories picked for each project. Molds and tools come from experienced partner toolmakers.`
→ `Need a part made from scratch? I make it too, through partner factories picked for each project. Molds and tools come from partner toolmakers.`

10. `From drawing to delivery, one accountable partner.`
→ `You send a drawing. I get the goods to your door.`

11. `Itemized cost breakdowns: materials, tooling, processing, finishing, logistics. No hidden lines.`
→ `Itemized quotes: materials, tooling, processing, finishing, logistics. No hidden lines.`

12. `Samples first, then mass production with scheduled quality checkpoints.`
→ `Samples first, then mass production, with quality checkpoints scheduled.`

13. `Every part is sampled and approved by you. Production begins only after you confirm.`
→ `You approve samples first. Production starts only after your confirmation.`

14. `Shipping overseas is included.`
→ `Shipping is part of the job, not your problem.`

15. `Real shipping dates in every quote, tracking in transit, a named contact who answers within 24 hours.`
→ `Real shipping dates in every quote, tracking in transit, answers within 24 hours: from me.`

- [ ] **Step 2: 校验**
`python -X utf8 scripts/check_copy.py --page index services` → 0 ERR 0 WARN。
- [ ] **Step 3: 提交**
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add index.html services.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v4: trader voice on index and services"
```

---

### Task 2: processes + deliveries + faq + about

**Files:** Modify: `processes.html`, `deliveries.html`, `faq.html`, `about.html`

**Interfaces:** Consumes Task V4-1 的声音基准；Produces 全站声音完成。

- [ ] **Step 1: 应用以下精确替换**（同样：old 串必须恰好出现一次，否则 STOP）

processes.html：

1. `Every process runs through partner factories, checked at each stage. Plastic, metal, foam, or parts to source: send the drawing and I'll tell you how I'd do it.`
→ `Every process runs through partner factories, checked at each stage. You send the drawing. I tell you how I'd do it.`

deliveries.html：

2. `Completed projects, delivered to clients overseas. Client names stay confidential.`
→ `Real projects, delivered to clients overseas. Client names stay confidential.`

faq.html：

3. `It depends on the supplier and the process. Every quote comes with a dated schedule you commit to, with shipping time quoted alongside.`
→ `It depends on the supplier and the process. Every quote comes with a dated schedule, and the shipping time is quoted right next to it.`

4. `Yes. I develop injection and rotomolding molds with my partner toolmakers, validate them with trial shots, and only then start production. You get mold drawings and a development schedule.`
→ `Yes. I develop injection and rotomolding molds with partner toolmakers, validate them with trial shots, then start production. You get mold drawings and a schedule.`

5. `Three checkpoints: (1) approved samples before mass production, (2) in-process and final random inspection, (3) a pre-shipment inspection report with photos. Third-party inspection available on request.`
→ `Three checkpoints: (1) samples approved by you before mass production, (2) in-process and final random inspection, (3) a pre-shipment report with photos. Third-party inspection available.`

6. `Yes. I prepare export documents, handle customs declaration, and arrange sea or air freight to your port or door.`
→ `Yes. Export documents, customs, sea or air freight to your port or door. I handle it.`

about.html：

7. `Six years in, he knows the production constraints and cost boundaries of multiple processes, and the practical details like logistics costs that decide whether a project lands on time and on budget.`
→ `Six years in, he knows what each process can and cannot do, what it costs, and the logistics math that decides whether a project lands on time and on budget.`

8. `The business runs on repeat orders and word of mouth, so every order matters. Without layers of middlemen, communication stays direct and open, and goals align with the client's: the right factory, a fair cost, and problems found and resolved early.`
→ `The business runs on repeat orders and word of mouth, so every order matters. Without layers of middlemen, goals align with the client's: the right factory, a fair cost, problems found and resolved early.`

- [ ] **Step 2: 校验**
`python -X utf8 scripts/check_copy.py --page processes deliveries faq about` → 0 ERR 0 WARN。
- [ ] **Step 3: 提交**
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add processes.html deliveries.html faq.html about.html
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v4: trader voice on processes, deliveries, faq, about"
```

---

### Task 3: 全站终验 + 同步 public/ + 提交

**Files:** Modify: `public/*.html`

- [ ] **Step 1: 全站校验**
`python -X utf8 scripts/check_copy.py` → 8 页 PASS 0 错误 0 警告。
- [ ] **Step 2: 同步**
```bash
cd "/d/YUKFO WED"
cp index.html services.html processes.html deliveries.html faq.html about.html contact.html thanks.html sitemap.xml public/
cp assets/css/style.css public/assets/css/style.css
```
`diff -rq --exclude=.git . public/` → 仅 "Only in" 行，零 "Files ... differ"。
- [ ] **Step 3: 提交**
```bash
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" add -A
git -c user.name="Jesus" -c user.email="hkyukfo@outlook.com" commit -m "copy v4: sync public/ with trader voice"
```
- [ ] **Step 4: 用户验收门**——停在任务外：向用户交付 18 处替换的逐条说明 + 本地预览（http://localhost:8931），用户点头后自行拖 public/ 部署。

---

## Self-Review（写计划时已跑）

1. **Spec 覆盖**：B 声音四规则 → 18 处替换全部落实（index 7 / services 8 / processes 1 / deliveries 1 / faq 4 / about 2）；contact 与 thanks 已在目标声音内零改动（明确写入约束 10）。✅
2. **占位符扫描**：无 TBD；18 对 old→new 全文给出。✅
3. **一致性**：新句经铁律逐条检查（无 we/无破折号/无绝对化词/无新事实/无数字承诺）；"samples checked before your money moves" 与 services 既有 bullet 同构（用户选 B 时明确接受此句）；FAQ #3 顺带修掉终审记过语法小晃（"you commit to"）。✅
4. **已知取舍（记录在案）**：用户否决过的"证据区"与 About Core Advantage 重写不进入本计划（尊重否决）；PAGE_BAND 1.10 维持（v4 只换句不新增，词数只会降不会涨）。✅
