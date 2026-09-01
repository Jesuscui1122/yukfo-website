---
name: geo-architecture-state
description: yukfo.com GEO 四站架构与部署真相（Workers Static Assets + yukfo-router）、构建系统、维护模式（2026-08-27 冻结）
metadata:
  type: project
---

# yukfo.com GEO 架构（2026-08-27 冻结，baseline commit a896744）

## ⚠️ 部署架构真相（下次会话必读，避免走弯路）

- **shiny-limit-af6b 是 Cloudflare Worker（Static Assets 模式），不是 Pages 项目**！Settings 显示 "Worker that only has static assets" 即是证据
- 全站跑在 Workers Static Assets 上：拖拽上传 dist/ 即更新静态内容（**不支持 Pages Functions**——拖拽上传器会报 "Pages functions are not supported"，且不支持 TypeScript）
- **路由层 = 独立 Worker `yukfo-router`**（Dashboard 创建，Hello World 起步）：按 hostname 转发到静态 Worker 的 workers.dev（`shiny-limit-af6b.179588752.workers.dev`）+ 目录前缀
  - us.yukfo.com → /us/、uk → /uk/、eu → /eu/、yukfo.com/www → 根
  - /assets/ 顶层共享；404 透传不 fallback
- 子域绑定：us/uk/eu.yukfo.com 在 yukfo-router 的 Domains；yukfo.com/www 在 shiny-limit-af6b
- 修改路由逻辑 = 改 yukfo-router 的 Worker 代码（Dashboard → Edit code），**与 dist/ 部署解耦**
- 线上地址（2026-08-27 验证）：四站 200，各站 title/hero/FAQ/schema 市场版生效

## 构建系统（新架构核心）

```
src/templates/*.html.template  ← 页面结构（占位符 {{field}}）
src/markets/{global,us,uk,eu}.json  ← 市场数据（SEO/hero/CTA/FAQ/area_served）
scripts/build.py               ← 零依赖生成器 → dist/
  - 生成 4 套：dist/（global 根）+ dist/us|uk|eu/
  - FAQ 数据驱动（页面 + FAQPage schema 同源）
  - JSON-LD 自动生成（Organization @id 按市场域名 + Service areaServed + FAQPage）
  - sitemap.xml + robots.txt 每市场生成；行尾随模板（CRLF/LF）
scripts/check_copy.py          ← 文案铁律：--dir 参数校验 dist/；市场必备事实表（US China team / UK accountable / EU quality checks+documentation）；index 基线 143（+How It Works）
scripts/verify_geo.py          ← build 后全量验证（title/meta/hero/schema/hreflang/sitemap/路由结构）
```

- **部署源 = dist/**（public/ 已退役，仅历史保留）；dist/、backups/ 已 gitignore
- 改文案 → 改 JSON → build → verify_geo → 拖 dist/ 部署
- 改公共结构 → 改模板 → 同上

## 内容状态（2026-08-27 冻结）

- 四站：global（Worldwide）/ us（United States）/ uk（United Kingdom）/ eu（Europe）
- hreflang 四向矩阵（eu 用 `en`，de-de 已移除）
- 首页：Hero（主+次级 CTA + 24h 回复行）+ How It Works 3 步 + Recent Work
- FAQ：global 8 / us 10 / uk 8 / eu 9；身份句 "No, I don't own factories..."（GEO Entity Definition 见 docs/geo-entity-definition.md）
- 联系方式已隐藏（表单唯一入口，FormSubmit jesus@yukfo.com 已激活验证 ✅）
- BR No. 已从首页移除（占位假号删除，待证书核验后加回，候选 80477500）
- 文案铁律全绿：check_copy 4 市场 PASS

## 冻结决策（用户拍板）

- **B3 Work 案例增强暂停**——不生成案例/数字/客户故事，等真实项目素材（格式预案：Product/Challenge/What I handled/Result）
- **/insights/ 内容资产暂缓**——等真实业务经验（客户常问/采购经历/真实项目）再整理
- **维护模式**：后续优化只基于真实客户反馈和业务数据；不新增功能、不改架构
- 用户风格：务实、防 AI 味、防编造；每步小步提交

## 2026-08-28 更新（文案收紧 + Work 9 张 + 图片标准）

- **文案收紧 10 处**（降承诺/去贸易公司味）：hero "No category limits"→"for custom products and components"、services 卡片（You name it / before your money moves / Made in partner factories / molds validated 全改）、FAQ ×4 市场（straight to the source / real cost data database 改）、contact notice（secure way→suitable way）、thanks（Nothing moves→Production starts after sample confirmation）、services why-not-factory（real cost data 追加发现也改）
- **Work 页 9 张**（用户最终定版）：吹塑瓶/注塑模具/铝型材/PVC型材/压铸件/滚塑铝模/滚塑铁模/五金/成品风扇（PRODUCT SOURCING / Alternative Product Solution）。4 张新素材图已处理（1200×900）
- **图片审核规则**：docs/image-selection-rules.md（3 秒识别测试/信息完整性优先/宁缺毋滥）；**work-images-approved/ 权威目录**（AI 不决定选图，用户放图→AI 只做技术处理）；03 铝型材、04 PVC 标注待替换（当前图识别度不足）
- **未提交 git**：今天所有改动（work 模板/文案/图片/规则文档）未 commit——明天先提交
- **待部署**：dist 9 张版已就绪未拖

## 2026-09-01/02 追加：UI 密集迭代收口（至 commit c20c774，已 push）

- **✅ 用户确认定稿（2026-09-02 "对了是这样的"）**：Work/Home 卡片图片 = hero 同款浮起效果（描边+16px 圆角+大投影+z-index 最上层+完整不裁切）；.case-card 去 border/overflow:hidden
- **最终态（用户逐轮确认）**：hero 图 = work-metal-assembly.jpg 完整显示（height:auto 无裁切）、hero 层 z-index:2 防下节遮挡、两栏 48px 偏移顶部齐平、hero 顶部 0；标题 2 行（question + accent span block + text-wrap:balance）；全站 .case-card img 无 aspect-ratio/object-fit（height:auto 完整显示），hover zoom 已删；HIW 标题竖线删除（.hero-split + .section h2::before display:none），HIW 段 margin-top:-52px + position:relative + bg 白 填入图片左侧空档；section 36px、卡片 gap 16px、container 1140
- **Work 页**：9 卡（回加 Plastic Components + Metal Parts，用首页同款图）；**hero 与卡片 1 不撞图**（hero=metal-assembly，card1=plastic-parts）
- **check_copy**：基线 index 136 / work 181；work 必备事实改 'references are available on request'（26-SKU 随 Programs 行删除）
- **⚡ 关键教训（重复 4+ 次）**：①**本地预览必须发 no-cache 头**——serve_local.py 已加 `Cache-Control: no-cache, no-store`，否则浏览器启发式缓存让用户连续看到旧页面，产生"没有变化"投诉；②**"没有变化"投诉先 curl/无头浏览器验证服务器产物，再考虑改代码**——本次曾盲改 3 轮；③**交付前用 playwright 无头截图自查**（npx playwright screenshot，浏览器已装），不要让用户当 QA——本次 15+ 轮往返的教训；④serve_local 用 ThreadingTCPServer（单线程版会被浏览器并行连接卡死）；⑤Windows 下预览服务器 CWD 占用 dist 导致 build rmtree 失败——改版前必须先杀 8897 进程（netstat+taskkill）
- **已 push**：42 commits（744d3bd..c20c774）备份至 GitHub ✓；**待办仅剩：用户拖 dist/ 部署 Cloudflare**

## ⚠️ 未结项（2026-09-02 收工时用户未认可）

- **PRODUCT SOURCING 详情页"看起来不行"**——用户最终反馈，具体哪里不行未说明。该页现有：照片墙 4 图（风扇主图 + LED/充电插座/摄像头，等比完整显示）+ 说明文字 2 行 + CTA。下次开场：请用户圈出问题点（截图圈注最有效），不要盲改
- **整个 dist/（今日全部改动）仍未部署**——线上 yukfo.com 还是 8 月旧版。部署 = 用户拖 dist/ 到 Cloudflare
- 已推送至 GitHub（6980ddc），本地与远程同步

## 2026-09-01 追加：定位改版落地（sourcing agent on the ground，commit e2982e1）

- **背景**：用户两条桌面指令（合并版）要求商业转化优化。两条定位冲突（"Manufacturing Partner" 商业味 vs "Founder-led sourcing agent" 个人味）——**裁决按后者**（与 8/9 以来全部已确认定位一致；指令一明文禁 "manufacturing partner"）；指令一的不冲突机械项（紧凑 hero/间距收紧/删弱项目/去灰框/按钮简化）全部吸收
- **文案**：hero "Need something from China? I'm your sourcing agent on the ground." + kicker "One contact. Multiple suppliers. Complete coordination."（模板硬编码，4 市场共用）；How It Works 三步改采购代理流程+删重复 CTA；services "What I Do"→"How I Help"（Supplier Sourcing/Supplier Verification/Order Management）；"Why Not Directly a Factory?"→"Why Work With a Sourcing Agent?"且上移到服务卡后；Processes/Materials 表降级到页底（深入了解阶段）
- **Work 页 9→7 卡**：删 PVC Extrusion Structural Profiles（图文不符——即原 04 待替换项，指令改为直接删项目）+ Steel Rotomolding Mold（客户难理解）；case-meta 灰框 chips 全删，改 Category/Title/一句价值（统一词表：sample verification/production follow-up/quotation comparison/delivery coordination，禁 supplier coordination/communication/sample review 重复）；图片已删（git 可恢复）；**04 PVC 待替换事项随项目删除而关闭**
- **SEO**：title/meta 织入 China sourcing agent/supplier verification/product sourcing from China（4 市场）；市场必备事实保留（us China team / uk accountable / eu quality checks+documentation）；check_copy 基线重校 165/528/179，4 市场 0 错误；verify_geo ALL PASSED
- **CSS**：.section 56→40px、hero-split 88/72→64/56px、lead mb 32→24px、新增 .hero-kicker（蓝 600）；移动端断点同比收紧（480 section 32px）——字体/颜色/导航/断点结构未动
- **未部署**：dist/ 已就绪待用户拖拽；根目录遗留旧版 *.html（GEO 前产物，非部署源）未动
- **注意**：8/27 维护模式冻结被本指令解除一次；check_copy HARD_WORDS 含 'trusted'（指令备选 hero "Your trusted person" 本就过不了校验）

## 2026-09-01 追加：中国大陆访问已封禁（用户要求）

- **Cloudflare WAF 自定义规则**（zone 级，1/5 免费额度）：`Block China traffic` = `(ip.src.country eq "CN")` → **Block**，Active
- 一条规则覆盖全部四站 + www（同 zone 子域名）
- **验证（2026-09-01 实测）**：本机直连 yukfo.com/us/uk/eu 全 403 ✅；走 clash 代理（127.0.0.1:33210）200 ✅；Google 爬虫（US IP）不受影响
- **自己看站**：直连打不开，必须走 clash/VPN（用户已确认接受）
- **解除方法**：Dashboard → Security → Security rules → 删除/禁用该规则，秒级生效
- 顺带效果：百度等中国爬虫也被拦（英文 B2B 站零损失）

## 待办（2026-09-01 核实更新）

1. ~~部署 9 张版 dist~~ ✅ **已上线**（2026-09-01 验证：www.yukfo.com/work/ 有 9 张 case-card，首页 hero 已是 "custom products and components" 新文案）
2. ~~git 提交 2026-08-28 改动~~ ✅ **已提交**（2026-09-01，commit 5ee4e4f，28 文件；git 身份已配到本仓库 repo-local：Jesus <hkyukfo@outlook.com>）
3. **Search Console**：添加 yukfo.com 域名属性（DNS TXT 验证）→ 提交 4 个 sitemap（yukfo.com/us/uk/eu）
4. BR 号：证书核验后加回首页
5. ~~git push~~ ✅ **已推送**（2026-09-01，8875156..d091d45，18 个提交直达 GitHub；第一次尝试 408 超时失败，repo-local `http.postBuffer 524288000` + 重试成功——以后 push 失败先试这个）
6. ~~铝型材/PVC 合格素材~~ **03 铝型材 ✅ 已替换并部署**；**04 PVC ✅ 事项关闭**（2026-09-01 定位改版按用户指令直接删除该 e2982e1 项目，不再等素材）
7. **部署定位改版 dist/**（commit e2982e1 产物，7 卡片版 + 新 hero）——待用户拖拽上传
8. 下次会话读本文件 + docs/geo-entity-definition.md + docs/image-selection-rules.md 后开工

相关：[[modern-simple-redesign]]（历史：4 页改版）、[[yukfo-email-warmup]]（邮箱预热）
