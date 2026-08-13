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
