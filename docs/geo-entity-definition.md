# YUKFO — GEO Entity Definition (Frozen 2026-08-27)

> 四站一致性基准。任何市场版本不得偏离本定义。
> 修改需用户确认。

## 实体定义（Entity Card）

```
YUKFO

Founder-led China sourcing partner
Based in China (Yangtze River Delta)
Works with partner factories, owns none
One accountable contact
```

## 身份表述（GEO 定义句，FAQ "Are you a factory?" 答案首句）

> No, I don't own factories. I work with partner factories and manage the sourcing process directly for clients.

## 四站矩阵

| 域名 | 市场 | hreflang | 内容语言 |
|---|---|---|---|
| yukfo.com | 全球默认 | x-default | English |
| us.yukfo.com | US 市场 | en-us | English |
| uk.yukfo.com | UK 市场 | en-gb | English |
| eu.yukfo.com | EU 市场 | en（非 de-de） | English |

## 各站只允许差异的字段

- SEO title / meta description
- Hero headline / subheadline
- FAQ 增补（市场痛点）
- 市场痛点表达
- JSON-LD（FAQPage / Organization @id / Service areaServed）

## 各站必须一致的字段

- 品牌（YUKFO）、人设（I / founder-led）、视觉结构、导航
- 实体定义（本文件）
- 禁止词（factory 能力表述 / cheap / low cost / guaranteed / fastest / trusted）
- 不承诺 MOQ / 固定交期 / 不可验证声明

## hreflang 规则

- 主站声明全部四向；子域页反向声明全部四向（双向对等）
- EU 子域用 `en`；未来增加德语版时再单独加 `de-de`
