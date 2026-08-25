# YUKFO 知识模型（2026-08-19 建立，路线 A：个人 agent + 制造知识升级）

> 本文件定义网站内容的结构化模型与事实标记规范。HTML 页面是真源，本文件是记录。
> 原则：信息可信 + 信息具体 + 信息互相连接 + 用户可以决策 + 用户可以行动。
> 铁律不变：不暗示自有工厂 / MOQ·交期零承诺 / 不自嗨 / clients overseas / 正文零破折号 / 不编造。

## 1. 实体与字段模型

### Process（工艺）
| 字段 | 要求 | 示例 |
|---|---|---|
| name | 准确工艺名 | Injection Molding |
| category | 分类 | Plastic Manufacturing |
| what it is | 一句话定义（事实） | Molten polymer injected into a closed mold |
| suitable for | 适合什么产品（事实） | pulleys, enclosures, brackets, housings |
| materials | 可用材料（真实覆盖） | PA6, ABS, PP |
| tolerances | 精度说明（**无实测数据写 "per part, quoted with drawings"，禁止编数字**） | — |
| finishes | 表面处理（真实做过才写） | texture, paint, pad printing |
| quantity | 数量适用性（不承诺 MOQ） | samples and trial runs first |
| tooling | 模具说明（真实） | molds from partner toolmakers, trial shots |
| limitations | 限制（诚实） | mold cost per part, geometry constraints |
| cost factors | 成本因素（不写死价） | material, part size, mold design, cycle time |
| verification | 事实标记 | VERIFIED / NEEDS_VERIFICATION |

### Material（材料）
| 字段 | 要求 | 示例 |
|---|---|---|
| name | 材料名 | PA6 (Nylon) |
| category | 金属/塑料 | Plastics |
| applications | 典型应用（事实） | bushings, pulleys, clips |
| properties | 特性（简短事实） | tough, wear-resistant, absorbs moisture |
| processes | 可用工艺（真实关联） | injection molding |
| finishes | 表面处理（有据才写） | — |
| notes | 注意事项 | — |
| verification | 事实标记 | — |

### Case（案例）
| 字段 | 要求 | 示例 |
|---|---|---|
| title | 匿名项目名 | Outdoor Blind System |
| client type | 匿名客户类型（不点名） | a hunting brand overseas |
| part | 造了什么 | 26-SKU prefabricated blind system |
| material | 材料（真实） | aluminum, PA, acrylic, EVA |
| process | 工艺（真实） | extrusion, injection molding, stamping, foam die-cutting |
| finish | 表面处理（有据） | — |
| quantity | 数量（真实才写，否则省略） | 26 SKUs |
| result | 结果（事实，不吹） | engineered, produced, checked, shipped as one program |
| verification | 事实标记 | — |

## 2. 关系（页面内互链）

- Process ↔ Material：processes 页每工艺列材料，materials 页每材料列工艺
- Material → Finishes：materials 页表面处理列
- Process → Case：deliveries 页工艺标签
- Home → Processes / Materials / Deliveries：能力总览矩阵链接
- Contact 上传入口是全局转化锚点

## 3. 事实标记规范（HTML 注释层，不上前台展示）

```html
<!-- VERIFIED: 2026-08-19 | source: PEXT808 RFQ evaluation | fact: 6063-T5 extrusion -->
<!-- NEEDS_VERIFICATION: 2026-08-19 | fact: typical tolerance range for injection molding -->
```

- VERIFIED：项目文档/报价/交付记录支撑
- SOURCE_BACKED：工艺大全知识库等外部调研支撑（含来源）
- NEEDS_VERIFICATION：无据，未上线公开内容，只允许出现在 Research Queue

## 4. Research Queue（docs/research-queue.md）

待验证项清单，每项：priority / reason / source / verification status / last updated。
首轮队列见 docs/research-queue.md（2026-08-19 建立）。
