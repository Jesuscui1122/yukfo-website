# yukfo.com 文案优化 v3 设计文档

> 日期：2026-08-13（第三轮，用户逐项确认）
> 状态：已获用户批准，待实施

## 背景

网站已正式上线（yukfo.com，2026-08-09），文案经 v1 建站 + v2 精修两轮。本轮用户决定：**用新模型对全站文本再做一轮优化**。

用户明确的范围与方向（逐条确认）：

1. **范围 = 文本**。视觉改版、analytics、SEO 技术项（robots.txt/canonical/JSON-LD）本轮不做。
2. **方向 = 地道感 + 去冗余**。修语态不统一、翻译腔、冗余重复。明确排除"营销腔/说服力优先"方向（沿用 v2 的排除项）。
3. **About = 第三人称 + 补主语**。开头一次点明主语（"the person behind YUKFO" 类，不公开姓名），后续 "he" 保留。故事内容不动。
4. **流程 = 样板先行（2+5）**。先重写 index + about 定基准，用户确认后批量过剩余 5 页。
5. **顺手项（获准）**：全站 `href` 多引号 bug 修复（clean URL 转换残留）；`DEPLOY.md` 更新为当前真实状态（7 页、已上线）。

## 铁律（沿用 v1/v2，锁定不碰）

1. 不暗示自有工厂（统一 "partner factories"，无 "my own production"）
2. MOQ/交期零承诺（不写数字，不暗示可控）
3. 不自嗨不绝对化（无 "always/everything"、无空修饰标签）
4. 不宣称具体地区（统一 "clients overseas"）
5. 正文零破折号（em-dash）、无 AI 模板句

## 本轮优化标准

1. **语态统一**：除 About 外全站第一人称 "I"；About 第三人称 + 开头补主语（不公开姓名）
2. **地道感**：消除翻译腔痕迹（如 "even everyday items"、"If your project needs it, it is in scope" 同页重复、"he" 无先行词），句式按英语母语习惯重排
3. **压缩冗余**：每句必须有信息量；整体词数目标 -20~30%；FAQ 答案直接回答，无铺垫
4. **忠于事实**：不增不减业务事实（报价拆项、QC 三步、工艺清单、26 SKUs、数字亮点等原样保留）
5. **微文案同样过**：meta 描述（顺手修 processes 页残留的 "trusted"——违反铁律 3）、按钮文案、表单 label/placeholder

## 逐页改动要点

| 页 | 要点 |
|---|---|
| index | hero 副句压缩；三卡片去水词；What We Do 压短；Why One-Person 压短 |
| about | 开头一次点明 "the person behind YUKFO"（不公开姓名），后续 he 保留；故事内容不动；数字 stat 不动 |
| services | **合并两个同名 "Product Sourcing" 区块为一个**（结构去重）；各段压缩 |
| processes | 5 个工艺描述压缩（工艺事实 + 行业 tag 保留）；meta 修 "trusted" |
| deliveries | 4 个项目描述压缩（26 SKUs 等事实保留） |
| faq | 10 条答案直接化，去铺垫句 |
| contact | 表单 label/placeholder 润色；Tip 框压短 |

## 交付与审阅流程

- **第一轮（样板）**：重写 index + about → 每页交付"逐条改动说明 + 新全文" → 用户确认风格基准
- **第二轮（批量）**：按确认基准过 services / processes / deliveries / faq / contact → 打包交付，格式同第一轮
- 审阅为纯文本形式；用户可随时要求本地预览渲染效果

## 部署衔接

1. 全部确认后：根目录 7 个 HTML → 复制进 `public/` → 用户拖拽上传 Cloudflare Pages（保持手动部署习惯）
2. 同步更新 `DEPLOY.md` 至当前真实状态（7 页、已上线、sitemap 已提交）
3. 顺手修复全站 `href="page""` 多引号（纯技术，不动文本）

## 验收标准

- 读起来像英语母语者写的，无翻译腔
- 全站语态通顺（About 的 he 有主语先行词）
- 无冗余句子，整体词数下降 20~30%
- 铁律零违反（含 meta 文本）
- 业务事实不增不减（除获准的 services 区块合并）

## 不在本轮范围

- 视觉改版（hero 加图、页面节奏、卡片样式）
- 数据分析（Cloudflare Web Analytics）
- SEO 技术项（robots.txt、canonical、JSON-LD、OG 图片、favicon、404 页）
- 表单提交后跳转页定制
