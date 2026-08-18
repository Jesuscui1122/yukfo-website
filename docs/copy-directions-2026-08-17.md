# 文案方向样片 A/B/C（2026-08-17，待用户选方向）

> 背景：v4 交易者声音用户仍不满意。诊断（用户确认三条）：
> ① 全站「I」字头句子 ~30 处，以自我为中心 ② You send X. I do Y. 句式单调、承诺感重 ③ 太空泛不具体（6 年/4 市场/26 SKU 只在 hero 数字条，正文无落地）
>
> 三版样片均满足：零 I 字头开头 / 句式长短变化 / 数字落实处。区别在语气调性。
> H1「Need something from China? I'm your sourcing agent. No category limits.」为已定定位，三版均保留（用户未要求动）。
> 约束（铁律不变）：无破折号 / partner factories（不暗示自有工厂）/ 不承诺 MOQ·交期数字 / 无绝对化 / clients overseas / 不复活"证据区"方案（用户 8/15 否决）。
> 样片打在首页核心区：hero 副题 + 三卡片 + 信任条。选方向后：整版重写 index → 用户过目 → 全站铺开 → check_copy.py → 同步 public/ → 部署 → 提交。

---

## 方向 A「你得到的」— 结果导向

- **hero 副题**：One drawing starts the whole chain: dated schedules, itemized quotes, samples you approve, goods checked before shipping. Six years in trade, four markets, one contact through it all.
  中：一张图纸启动整条链：日期化排期、分项报价、你确认的样品、发货前验过的货。六年贸易经验、四个市场、从头到尾一个联系人。
- **卡片 1**：You describe the part, I find the factory. Quotes compared across suppliers against real cost data, samples checked before your money moves.
  中：你描述零件，我找工厂。多供应商比价、对照真实成本数据，付款前样品先验。
- **卡片 2**：Your drawing becomes parts: injection, rotomolding, extrusion, foam, metal, through partner factories. Samples approved by you before production.
  中：你的图纸变成零件：注塑、滚塑、挤出、发泡、金属，走合作工厂。投产前样品由你确认。
- **卡片 3**：One schedule covers sourcing, tooling, production, inspection, documents, shipping. One contact answers for all of it.
  中：一张排期表管住找料、开模、生产、验货、单证、物流。一个联系人为此负责。
- **信任条**：Repeat orders carry this business. That means quotes itemized line by line, schedules with real dates, and a photo report before shipment.
  中：这生意靠返单活着。所以报价逐行分项、排期写真实日期、出货前有照片报告。

## 方向 B「你不必操心的」— 减负式

- **hero 副题**：No layers of middlemen. Emails answered within a day. No hidden lines in a quote. A drawing in, the chain runs: dated schedule, approved samples, goods checked at your port or door.
  中：你和工厂之间没有中间层。邮件当天有回音。报价单没有隐藏项。图纸进来，链条跑起来：日期化排期、确认过的样品、验过的货到你港口或门口。
- **卡片 1**：One request, and the comparison comes back: suppliers, cost data, sample checks. You approve before money moves.
  中：一个请求，对比就回来：供应商、成本数据、样品检验。钱动之前你先点头。
- **卡片 2**：Partner factories, chosen for your project. You approve the samples; production waits for your confirmation.
  中：合作工厂，按你的项目挑。样品你确认，生产等你点头。
- **卡片 3**：Documents, customs, freight: handled in one chain. Tracking in transit, answers within 24 hours.
  中：单证、报关、货运：一条链办完。物流可查，24 小时内有回音。
- **信任条**：This business runs on referrals. One wrong order costs the next one, so every order gets the same care: itemized quotes, dated schedules, photo reports.
  中：这生意靠口碑活着。一单做错就丢下一单，所以每单同样用心：分项报价、日期化排期、照片报告。

## 方向 C「平实陈述」— 克制式

- **hero 副题**：6 years in cross-border trade. 4 markets served. 26 SKUs delivered in one program. A drawing arrives, and you get back a dated schedule and an itemized price.
  中：跨境贸易 6 年。服务 4 个市场。单个项目交付 26 个 SKU。图纸进来，回给你的是日期化排期和分项报价。
- **卡片 1**：Standard or custom components, found and verified: quotes compared against cost data, samples checked, export paperwork done.
  中：标准件或定制件，找到并验过：比价对照成本数据、样品验过、出口单证办妥。
- **卡片 2**：Injection, rotomolding, extrusion, foam, metal, in partner factories. Molds from partner toolmakers, validated with trial shots.
  中：注塑、滚塑、挤出、发泡、金属，在合作工厂做。模具出自合作模具厂，试模验证过。
- **卡片 3**：From drawing to delivery: sourcing, tooling, production, inspection, documents, shipping. One person holds the schedule.
  中：从图纸到交货：找料、开模、生产、验货、单证、物流。一个人握着排期。
- **信任条**：The orders that matter most are the next ones. Quotes itemized, schedules dated, shipments photo-checked: the terms clients can hold me to.
  中：最重要的订单是下一单。报价分项、排期写日期、出货照片验货——这些是客户可以拿来要求我的条款。

---

## 明天接续点

1. 用户选方向（A/B/C 或提出修改）
2. 整版重写 index → 过目
3. 全站铺开（services/processes/deliveries/faq/about/contact）
4. `python -X utf8 scripts/check_copy.py`（0 错误）
5. 同步 `cp *.html sitemap.xml public/`
6. 提交 git（`-c user.name="Jesus" -c user.email="hkyukfo@outlook.com"`）
7. 拖 public/ 到 Cloudflare 部署

⚠️ 当前工作区状态：6 处去重改动（index/services/about，root+public/）已改未提交未部署；SEO canonical 修复已提交 9041d81 已部署。
