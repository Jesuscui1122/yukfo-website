# YUKFO 研究队列（Research Queue）

> 机制：发现知识缺口 → 记录 → 验证 → 上线。禁止跳过验证直接编造上线。
> 状态：PENDING（未验证）/ IN_PROGRESS / VERIFIED / DROPPED

## 首轮队列（2026-08-19 建立）

| # | 任务 | 优先级 | 原因 | 来源 | 状态 | 更新 |
|---|---|---|---|---|---|---|
| RQ-1 | 注塑公差范围（真实工厂口径） | P1 | processes 知识化需要，禁止编数字 | 工艺大全知识库 + 供应商确认 | PENDING | 2026-08-19 |
| RQ-2 | 滚塑壁厚/尺寸上限 | P1 | processes 知识化需要 | 工艺大全 + 供应商确认 | PENDING | 2026-08-19 |
| RQ-3 | 挤出型材典型公差 | P1 | processes 知识化需要 | 工艺大全 + 供应商确认 | PENDING | 2026-08-19 |
| RQ-4 | 阳极氧化兼容材料清单 | P2 | materials 页表面处理列 | 工艺大全材料档案（有） | PENDING | 2026-08-19 |
| RQ-5 | EVA/IXPE 密度范围与切割精度 | P2 | processes 发泡知识化 | 工艺大全档案 + 参考价目表 | PENDING | 2026-08-19 |
| RQ-6 | 锌压铸典型件重/壁厚 | P2 | processes 金属知识化 | 工艺大全 + 供应商 | PENDING | 2026-08-19 |
| RQ-7 | 铝 6063 表面处理选项核实（阳极/染色/喷涂） | P1 | PEXT808 案例 finish 字段 | PEXT 项目记录（染色黑已确认 DR-021） | VERIFIED | 2026-08-19 |
| RQ-8 | camera 420TVL/IP68 参数可否公开上案例 | P1 | deliverables 案例字段 | Safe 报价单（真实） | IN_PROGRESS | 2026-08-19 |
| RQ-9 | FormSubmit 免费版附件大小上限 | P2 | contact 上传字段 | formsubmit.co 文档 | PENDING | 2026-08-19 |

## 使用规则

1. 新增缺口先登记再处理，登记时必须写 reason + source
2. 验证完成 → 更新状态 → 上线内容（HTML 加 VERIFIED 注释）
3. 无源可验证 → 保持 PENDING，不编造上线
