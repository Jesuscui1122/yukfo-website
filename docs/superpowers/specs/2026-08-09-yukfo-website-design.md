# yukfo.com 官网设计文档 v1

> 日期：2026-08-09
> 状态：已获用户批准（2026-08-09，全部决策逐条确认）

## 1. 项目定位

**一句话**：Yukfo = Jesus，一个为海外买家提供"项目落地"服务的制造伙伴。

**核心价值主张**（用户确认）：
- 客户带图纸/概念，Yukfo 负责把项目变成交付的产品
- 自己能做的工艺自己做；做不了的帮客户找对的人做（Product Sourcing）
- 定位是**个人服务商**，不装公司、不装工厂

**明确不做的事**：
- ❌ 不展示"我们拥有"的机器/车间照片（无自有工厂，冒充会毁掉信任）
- ❌ 不从网上扒产品图（版权 + 客户反向搜图信任崩塌）
- ❌ 不发布价格（B2B 制造走询盘，不挂价目）
- ❌ 不放阿里国际站/中国制造网店铺链接（用户确认：客户会绕过中间人直连工厂）

## 2. 目标受众

- 北美（美/加）、欧洲（奥地利等）、拉美（厄瓜多尔/委内瑞拉）采购商
- 决策人：产品经理/采购/创业公司创始人（如 SPADE、Golfinho、ACCUFORM 这类品牌客户）
- 全英文网站，无中文版（v1）

## 3. 网站结构（5 页，全英文）

| 页面 | 内容 |
|---|---|
| **index.html (Home)** | Hero（一句话定位）+ 3 服务入口（制造/寻源/项目管理）+ 行业案例缩略 + 询盘 CTA |
| **services.html** | 三大服务块：Custom Manufacturing（6 工艺：注塑/滚塑/挤出/发泡模切/金属加工/电子组装 + 模具开发）· Product Sourcing（超出自有工艺的产品寻源）· Turnkey Project Delivery（图纸→交付全程管理） |
| **industries.html** | 4 行业案例：Outdoor & Hunting（猎屋 26 SKU 系统）· Water Sports（桨/船体/配件）· Home & Building（门窗型材/水箱/花盆）· Electronics（开关面板/摄像头/智能锁） |
| **about.html** | 个人故事：5 年外贸（美/加/厄/委/奥市场）、"我的生意是信誉，利益绑定"、成本透明度 |
| **contact.html** | 询盘表单（产品描述/数量/目标价/交期）+ 邮箱 + WhatsApp |

导航：5 页顶部导航 + 移动端汉堡菜单。页脚：品牌名 + 邮箱 + 版权。

## 4. 视觉设计

- 风格：极简白（纯白底/黑白灰/1px 细线/小圆角 2px/无网格无阴影），深蓝 `#1e3a5f` 点缀（主按钮/选中态/标题左竖线/表头）——沿用用户在工艺大全 APP 验证并确认的偏好
- 字体：系统字体栈（避免外部字体加载拖慢海外访问）
- 响应式：桌面优先，移动端汉堡导航
- 首页样式变体：实施时做 2-3 个 hero 变体供用户浏览器预览对比（沿用工艺大全皮肤对比流程）

## 5. 技术架构

- 纯静态 HTML/CSS/JS，零框架零依赖（v1 不用构建工具）
- 文件结构：`assets/css/style.css`、`assets/js/main.js`、`assets/images/{industries,generated}/`
- 部署：Cloudflare Pages（免费，全球 CDN，自动 HTTPS）
- 域名：yukfo.com 已在 Namecheap（URL 转发停靠状态）→ 上线时关闭 URL 转发，DNS 切 Cloudflare NS
- 询盘表单：Formspree/Web3Forms 免费档转发邮件；**收件邮箱写入独立配置文件，用户未定邮箱，默认 hkyukfo@outlook.com，后续随时可改**
- SEO：每页 meta description、语义化 HTML5、Open Graph 分享卡片；上线后提交 Google Search Console
- 联系方式：邮箱（待定域名邮箱 vs outlook，用户未决定，不阻塞）

## 6. 素材方案

**图片铁律**（用户确认）：所有图必须符合"我是做这些事的人"，而非"我是拥有这些设备的人"。

| 用途 | 来源 | 状态 |
|---|---|---|
| 行业场景图（kayak/户外/家居等，Industries 页示意） | Unsplash 免费图库（images.unsplash.com 可达；Wikimedia 被墙、Pexels 403） | 待下载 |
| AI 生成示意图（图库缺失场景，如滚塑/挤出/发泡产线氛围） | DashScope 万相（DASHSCOPE_API_KEY 已配置） | 待生成 |
| 产品实拍（最关键） | 用户手机自拍 + 合作工厂实拍（Gonuo/Hehua/江阴华宇等） | **用户负责，持续收集** |
| Logo | 用户提供文件（未注册商标，不加 ™/®） | 待用户提供 |
| About 个人照（可选） | 用户自拍 | 可选 |

**候选 CAD 渲染**（v1 不依赖）：用户有大量 STP/DWG 文件（船.stp、SPADE SLICK mold.stp、花盆.dwg），环境当前无 trimesh/cadquery，可后续 pip 安装后渲图作为产品图补充。

## 7. 内容计划

- 我起草全部英文文案初稿，用户审阅修改
- 关键文案（已确认方向）：
  - Hero：*"Your project, delivered. From drawings to finished goods — custom manufacturing, product sourcing, and full project management for outdoor, marine, and home products."*
  - About：5 年跨境贸易、服务市场、利益绑定话术（"我的生意是信誉，每一单都是回头单的赌注"）
  - 工艺卡片：材料、典型产品、真实案例（来自参考价目表与项目文件）

## 8. 上线流程（第 4 周）

1. Cloudflare 注册账号（免费）
2. 构建产物部署到 Cloudflare Pages
3. Namecheap 关闭 URL 转发 → 域名 DNS 改到 Cloudflare（用户操作，我逐步指导）
4. 验证 HTTPS 生效、全球可达、表单转发通
5. 提交 Google Search Console + Bing Webmaster

## 9. 时间线（上线目标：2026-09-09 前）

- W1（8/9-8/16）：设计定稿 ✅ + 建站骨架 + 英文文案初稿
- W2（8/17-8/23）：文案终稿 + 素材收集（用户拍产品照/要工厂图 + 我下载图库/AI 生成）
- W3（8/24-8/30）：视觉打磨 + hero 变体对比 + 表单联调 + 全页检查
- W4（8/31-9/6）：部署 + DNS 切换上线 + 收录提交

## 10. 风险与边界

- 邮箱未定 → 不阻塞，配置文件默认 outlook，随时可换
- Logo 未提供 → 先用文字标 YUKFO 占位，Logo 到位后替换
- 产品实拍未到位 → 上线时可用行业示意图 + AI 生成图支撑，实拍后持续替换（图片路径约定不变）
- AI 生成图仅用于氛围/示意，不用于产品展示（避免虚假产品承诺）
- 网站内容不承诺产能/认证（无 ISO 认证，不打工厂牌）
