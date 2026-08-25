# Yukfo.com 现代极简改版 — 设计文档

**日期:** 2026-08-25
**状态:** 用户批准（口头"开始"）
**参考:** techfo.com.hk（只借鉴"简单的结构"，不照抄复古视觉）

## 1. 背景与目标

用户看到 techfo.com.hk 后提出"想与这个网站差不多"。经三轮澄清，用户真正想要的是：

- **简单**：区块少、文字少、不复杂（techfo 的结构：一个标语 + 满屏图 + 极简导航）
- **现代**：不要 techfo 的复古感（Wix 老模板、旧字体），要当代设计语言（大留白、Inter、圆角、微动效）
- **真实案例信任感**：用真实产品图说话，不靠文字吹

**不是**：不要黑底、不要照抄 techfo 布局、不推翻 8/23 拍板的保守白底深蓝基调（圆角/hover 等"现代感"元素本次解锁）。

## 2. 现状资产盘点（保留清单）

| 资产 | 去处 |
|---|---|
| hero 主句 "Need something from China? I'm your sourcing agent." | 保留（新 hero 左侧） |
| Services 页工艺矩阵表（6 工艺）+ 材料表（8 材料） | 保留（services.html 精简后） |
| FAQ 内容（Who is YUKFO / Are you a factory / Pricing transparency / quality） | 迁移至 contact.html 折叠区，精简至 6-8 问 |
| deliveries case-meta 数据（Part/Material/Process/Finish/Quantity/Result） | 迁移至新 work.html |
| 表单（FormSubmit → jesus@yukfo.com，_replyto/reCAPTCHA/_next/_autoresponse） | 保留 |
| _redirects 301 规则、canonical、sitemap、noindex thanks | 保留并更新 |
| WhatsApp 按钮（wa.me/8617860570306）、域名邮箱 | 保留 |
| 实体行（Yukfo Limited · Hong Kong） | 保留（首页底部 + 页脚） |

**删除页面:** deliveries.html、faq.html（root + public 双份）

**注意（未决风险，非本改版范围但部署前必办）:** BR No. 12345678 为占位，候选 80477500 需用户注册证书核验后替换；FormSubmit 需 jesus@yukfo.com 激活验证。

## 3. 页面结构（4 页 / 4 导航）

导航：**Home / Services / Work / Contact**（毛玻璃吸顶，现有实现保留）

### 3.1 Home（index.html）

```
Hero（左文右图）：
  左：kicker "Sourcing Agent · Hong Kong"（小字，可省）
      H1 "Need something from China? I'm your sourcing agent."
      副句（一句话，无破折号）
      深蓝按钮 "Start a project"（圆角 10px）
  右：产品图一张，4:3 大圆角卡片，微 hover
精选案例（3 张）：
  3×1 横排（桌面）/ 纵向（移动），一图一标题，点击进 Work 页
底部（一行）：
  jesus@yukfo.com · WhatsApp · Yukfo Limited · Hong Kong
无其他区块。
```

### 3.2 Services（services.html，精简）

- 一句话 intro
- 三块能力：Sourcing / Manufacturing / Turnkey（短，各 1-2 行）
- 工艺矩阵表（6 工艺，含 Limits 列，现有内容）
- 材料表（8 材料，现有内容）
- "为什么不直接找工厂"一节（现有 FAQ 答案精华）
- 现有 hero/信任条等冗余区块删除

### 3.3 Work（work.html，新建）

- 页头一句话
- 案例全集：6-9 张真实产品图，网格 3×2 / 3×3，一图一标题
- 点击放大（lightbox，原生 JS 简单实现）
- 每案例下方/悬停显示 case-meta（Part/Material/Process/Finish/Quantity/Result，从 deliveries 迁移的真实数据）
- 案例图 **全部为用户提供的真实图**，不用 AI 图

### 3.4 Contact（contact.html）

- 表单（现有 FormSubmit 配置原样保留）+ WhatsApp + 邮箱
- FAQ 折叠区（6-8 问，从 faq.html 精简迁移，details/summary 无 JS 实现保留）

## 4. 视觉规范（现代极简）

| 项 | 值 |
|---|---|
| 背景/文字 | #fff / #111（标题）、#555-666（正文） |
| 品牌色 | 深蓝 #1e3a5f（按钮/强调/链接） |
| 点缀 | 金黄 #e6b83c（少量，hover/标记） |
| 字体 | Inter（已引入），标题 600-800 字重，正文 400 |
| 圆角 | 10-14px（卡片/按钮/图片） |
| 留白 | 区块垂直 padding ≥ 100px，大标题 38-60px |
| 微动效 | 卡片 hover 上浮 1-2px + 图片缩放 1.02-1.05；导航毛玻璃（已有） |
| 阴影 | 极轻，仅卡片 hover 态（box-shadow 0 4px 20px rgba(0,0,0,.06)） |
| 响应式 | 三档断点已有（1024/768/480），图片网格降列 |

**明确不做（YAGNI）:** 黑底深色主题、复杂动效/滚动渐入 JS、亮蓝 #1A56DB、badge、深色 footer、多列 hero 之外的布局实验。

## 5. 文案规则（铁律全保留）

- 不暗示自有工厂（统一 "partner factories"）
- MOQ/交期不写数字不承诺
- 不自嗨不绝对化
- 正文零破折号（head title 除外）
- 无 AI 味、不宣称具体服务地区

新文案示例（hero 副句）:
> "From a single part to a full product line. I find it, verify it, and deliver it."

## 6. 素材清单

**用户提供（必填，阻塞上线）:**
- 6-9 张真实产品图（手机实拍/供应商图/客户产品照均可），如：HUNT T-Handle Lock、Acrylic Panels、车载摄像头、滚塑浮体、铝型材、橙子箱等
- 统一处理：裁切 4:3、压缩 WebP/JPEG ≤ 200KB、命名 `work-*.jpg` 入 `assets/images/work/`

**hero 右图:** 从上述图中选最出彩一张。

**图未到位时:** 页面骨架先搭，图位占位，上线阻塞（不放 AI 图顶替）。

## 7. 技术实现

- 纯静态 HTML/CSS/少量 JS（lightbox），现有体系不变
- lightbox：原生 JS（~30 行）或现有依赖，无新框架
- 全站 4 页 + thanks（noindex）
- root 与 public/ 双份同步（现有工作流）
- check_copy.py 校验 + 词数基线重校
- sitemap.xml → 4 URL + thanks 排除；canonical 更新；_redirects 更新：
  - `/deliveries` `/deliveries.html` → `/work`
  - `/faq` `/faq.html` → `/contact`
  - 其余保留

## 8. 实施顺序

1. 用户提供真实产品图 → 裁切/压缩入 assets
2. index.html 重构（B hero + 精选 3 图）
3. work.html 新建（案例全集 + case-meta + lightbox）
4. services.html 精简
5. contact.html 加 FAQ 折叠；删 faq.html、deliveries.html（root+public）
6. _redirects / sitemap / canonical 更新；check_copy 重校；双份同步
7. 本地预览（serve_local.py :8897）用户过目
8. BR No. 替换（需证书核验）→ 提交 → push → 部署 public/
9. FormSubmit 激活验证 + 附件上传实测（RQ-9）

## 9. 验收标准

- 4 页 4 导航，滚动无多余区块
- 现代极简视觉（Inter/深蓝/圆角/留白/hover）
- 案例全为真实图，点开放大，case-meta 数据真实
- check_copy 0 错误；root/public 一致；移动端零溢出
- 表单提交可收信（激活后）
- 线上 4 URL 200，旧 URL 301

## 10. 范围外（后续再说，不阻塞）

- schema.org 结构化数据
- 附件上传真机实测（RQ-9，部署后）
- 多语言版
