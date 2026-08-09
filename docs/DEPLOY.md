# yukfo.com 部署手册（Cloudflare Pages，免费）

> 状态：**待执行**（上线周 W4：2026-08-31 ~ 09-06 执行，目标 09-09 前上线）
> 前置：设计已定稿（hero A 版）、5 页 + 素材已就绪、本地评审全绿

## 0. 上线前检查（先做，10 分钟）

```bash
cd "/d/YUKFO WED"
python -X utf8 -m http.server 8760   # 本地预览
```
浏览器检查：
- [ ] 5 页均可访问、导航高亮正确
- [ ] 桌面 + 手机（375px）布局正常
- [ ] 图片加载正常（industries 4 张 + logo）
- [ ] 页脚邮箱 `hkyukfo@outlook.com` 正确

## 1. Cloudflare 部署（30 分钟）

1. 注册 Cloudflare 账号（免费）：https://dash.cloudflare.com/sign-up
2. 左侧菜单 → **Workers & Pages** → **Create** → **Pages** → **Upload assets**
3. 项目名：`yukfo`
4. 上传构建产物：**本地目录 `D:\YUKFO WED` 中除以下内容外的全部文件**（上传目录模式直接拖拽整个文件夹）
   - ❌ 不传：`.git/`、`docs/`（含 superpowers/ 和 review/）、`scripts/`（生成脚本含 API 逻辑，不该公开）、`assets/images/README.md`（可传可不传）
   - ✅ 必传：`index.html` `services.html` `industries.html` `about.html` `contact.html` + `assets/`（css/js/images）
   - 建议先在项目里建一个 `public/` 目录放这些文件再上传（见步骤 5 替代方案）
5. **（替代方案，更干净）** 建发布目录：

```bash
mkdir "/d/YUKFO WED/public"
cd "/d/YUKFO WED"
cp index.html services.html industries.html about.html contact.html public/
cp -r assets public/
# 然后上传 public/ 整个目录
```

6. 部署完成后 Cloudflare 会给一个 `*.pages.dev` 地址，先验证这个地址 5 页全通、HTTPS 正常

## 2. 域名接入（Namecheap → Cloudflare，15 分钟）

**在 Namecheap 侧操作（用户执行，我逐步指导）：**

1. Namecheap 控制台 → **Domain List** → yukfo.com → **Manage**
2. 左侧 **URL Forwarding** → 找到现有的 `http://yukfo.com` 转发 → **删除**（否则和网站冲突）
3. 左侧 **Advanced DNS**：
   - 删除旧的 A Record / CNAME（Namecheap 停靠页的记录）
   - 保留/确认 MX 记录（如果有邮箱用，先查有没有 MX 记录——有的话别删）
4. 回到 Cloudflare Pages 项目 → **Custom domains** → **Add custom domain** → 输入 `yukfo.com`
   - Cloudflare 会提示添加 CNAME 记录：`www` → `yukfo.pages.dev`（在 Namecheap 里加这条 CNAME）
   - 再添加：裸域 yukfo.com 的 CNAME 指向 `yukfo.pages.dev`（Namecheap 支持根域名 CNAME 则直接用，不支持则用 Cloudflare 的 "Redirect" 方案：把 yukfo.com 的 A 记录指向 `192.0.2.1` 假 IP + 在 Cloudflare 开一个重定向规则，或者最简单——只绑定 `www.yukfo.com`，然后把裸域 301 转到 www）
5. **Nameservers 切换（可选但推荐）**：Namecheap Advanced DNS → Nameservers → Custom DNS → 填 Cloudflare 分配的两个 NS（`xxx.ns.cloudflare.com`）
   - 切换后 DNS 生效时间：几分钟到 48 小时（一般 1-2 小时内）
   - 切换后 SSL 证书由 Cloudflare 自动签发

## 3. 验证上线（15 分钟）

```bash
curl -I https://yukfo.com          # 期望 200 + cf-ray 头
curl -I https://www.yukfo.com      # 期望 200（或 301 到裸域/www，取决于绑定方案）
curl -s https://yukfo.com/services.html | head -5
```
- [ ] HTTPS 证书有效（浏览器无警告）
- [ ] 5 页全通、图片加载、表单可提交
- [ ] 手机浏览器打开正常

## 4. 表单联调（首次必须做）

1. 在线上 contact 页**真实提交一次**询盘（填自己的邮箱）
2. 收件邮箱 `hkyukfo@outlook.com` 会收到 FormSubmit 的**激活邮件** → 点激活（只此一次）
3. 再提交一次确认邮件到达、内容字段完整（Name/Email/Product description 等）
4. 之后每个询盘自动转发到邮箱

## 5. 搜索引擎收录（上线后 1 天内）

1. https://search.google.com/search-console → 添加 `yukfo.com` → 按提示验证（Cloudflare Pages 已自动带验证 meta 则选 HTML 标签方式，或 DNS TXT 验证）
2. 提交首页 URL 请求收录
3. Bing Webmaster 可选（流量占比小）

## 6. 后续维护备忘

- **改邮箱**：contact.html 表单 action 里的 `hkyukfo@outlook.com` + 页脚 mailto（两处，已注释标注）
- **改文案**：直接改对应 HTML 文件 → 重新上传 public/ → 部署自动生效（Cloudflare Pages 上传模式每次手动拖新目录）
- **加产品图**：assets/images/ 加文件 → 上传
- **重要提醒**：部署目录不含 docs/ 和 scripts/——上传时务必用 public/ 目录，不要直接拖整个项目根

## 7. 上线周行动清单

- [ ] 用户提供产品实拍图（如有，替换 industries 图或加进首页）
- [ ] 决定是否配域名邮箱 jesus@yukfo.com（可选，Google Workspace $6/月 或 Namecheap 免费额度）
- [ ] 执行本手册第 1-5 步
- [ ] 上线后持续收集询盘数据
