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

## 待办（2026-09-01 核实更新）

1. ~~部署 9 张版 dist~~ ✅ **已上线**（2026-09-01 验证：www.yukfo.com/work/ 有 9 张 case-card，首页 hero 已是 "custom products and components" 新文案）
2. ~~git 提交 2026-08-28 改动~~ ✅ **已提交**（2026-09-01，commit 5ee4e4f，28 文件；git 身份已配到本仓库 repo-local：Jesus <hkyukfo@outlook.com>）
3. **Search Console**：添加 yukfo.com 域名属性（DNS TXT 验证）→ 提交 4 个 sitemap（yukfo.com/us/uk/eu）
4. BR 号：证书核验后加回首页
5. ~~git push~~ ✅ **已推送**（2026-09-01，8875156..d091d45，18 个提交直达 GitHub；第一次尝试 408 超时失败，repo-local `http.postBuffer 524288000` + 重试成功——以后 push 失败先试这个）
6. 铝型材/PVC 合格素材：用户放入 work-images-approved/ 后 AI 替换+build
7. 下次会话读本文件 + docs/geo-entity-definition.md + docs/image-selection-rules.md 后开工

相关：[[modern-simple-redesign]]（历史：4 页改版）、[[yukfo-email-warmup]]（邮箱预热）
