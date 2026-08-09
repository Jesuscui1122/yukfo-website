# yukfo.com 文案精修 v2 设计文档

> 日期：2026-08-09（第二轮 brainstorming，用户逐页确认）
> 状态：已实现并提交（master 476eea9 及之前提交）

## 背景

网站 v1 已建成（7 页），用户评估后认为**文本需要改善**，启动第二轮梳理。目标：**准确（业务事实）+ 简洁 + 自然口语**（明确排除"更有说服力/营销腔"方向）。

## 本轮确认的关键业务决策

1. **收费模式：贸易商加价（+15-20%）**——用户最终决定，弃用"工厂价+明确服务费"方案。网站不公开收费模式细节，保持 "Itemized cost breakdowns... No hidden lines"（报价拆项为真实事实）
2. **客户来源：老客户/转介绍 + 主动开发为主**（非平台询盘）→ 网站角色 = 主动开发时的**信任背书**：5 秒看懂你是谁、10 秒信任、30 秒知道怎么联系
3. **MOQ 边界**：MOQ 由工厂定，文本零数字承诺、零"我能控制"暗示
4. **交期边界**：不承诺具体周数，随报价确认排期

## 文本改善原则（本轮标准）

- 删自嗨标签（hands-on、trusted、the right supplier、real prices 等空修饰）
- 去 AI 味（破折号 66→16，正文清零；模板句打散；被动语态改主动——注意去自嗨时改过头成被动语态，本轮修正回来）
- 不宣称具体地区（统一 "clients overseas"）
- 不承诺无法控制的事（MOQ/交期/无意外）
- 忠于用户定稿内容（About 故事仅润英文，不动内容）

## 逐页改动摘要

| 页 | 改动 |
|---|---|
| index | hero 问句开场；副标题拆短；"stays accountable"→"handles it all"；卡片去空修饰；What We Do 导语去重复 |
| services | Sourcing 导语被动→主动（修正改过头）；列表动词开头；Custom Manufacturing 导语简化（picked/come from） |
| processes | How It Works 导语简化（删 trusted） |
| deliveries | 3 处项目描述精简（through production 删、两句并一句、and→or） |
| about | 副标题删 hands-on+地区→overseas；Expertise 段精简 |
| faq | 之前已改：MOQ 零承诺、交期随报价、样品费见数、直接回答 |
| contact | 之前已改：direct answers |

## 剩余事项

- FAQ/Contact 本轮未动（前轮已精修）
- 部署未做（用户决定不急于上线）
- W4（8/31-9/6）接入 yukfo.com 正式域名
