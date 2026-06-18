# academic-pipeline

**一句话定位**：学术研究 → 论文发表的全流程编排器。10 阶段状态机 + 强制完整性门控 + 两阶段同行评审 + 可重复质量追踪。

> 基于 [Cheng-I Wu / academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v3.7.0 改编，适配 WorkBuddy 单 agent 架构。

---

## 快速上手

### 安装

将 `academic-pipeline` 文件夹复制到你的 Skill 存储路径：

```
# WorkBuddy 用户级
~/.workbuddy/skills/academic-pipeline/

# 或项目级
<project>/.workbuddy/skills/academic-pipeline/
```

### 依赖 Skill

academic-pipeline 是**编排器**，本身不执行实质性工作。以下 Skill 需预先安装：

| 阶段 | 依赖 Skill | 最低版本建议 |
|------|-----------|-------------|
| Stage 1 | `deep-research` | ≥ 3.0 |
| Stage 2 | `academic-paper` | ≥ 4.0 |
| Stage 3/3' | `academic-paper-reviewer` | ≥ 3.0 |
| Stage 5 | `academic-paper`（format-convert） | ≥ 4.0 |

### 触发词

**中文**：学术流水线、研究到论文、完整论文流程、端到端论文、研究到发表
**英文**：academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper

---

## 架构概览

```
 ┌──────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐
 │ RESEARCH │──▶│  WRITE   │──▶│ INTEGRITY │──▶│  REVIEW  │
 │ (Stage1) │   │ (Stage2) │   │ (Stage2.5)│   │ (Stage3) │
 └──────────┘   └──────────┘   └───────────┘   └──────────┘
                                                        │
                                          Accept ───────┤────── Reject → 回 Stage2
                                          Minor/Major ──┤
                                                        ▼
 ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌───────────┐
 │  REVISE  │──▶│RE-REVIEW │──▶│RE-REVISE │──▶│FIN.INTEG. │
 │ (Stage4) │   │ (Stage3')│   │ (Stage4')│   │ (Stage4.5)│
 └──────────┘   └───────────┘   └──────────┘   └───────────┘
                                                        │
                                          PASS ─────────┤────── FAIL → 修复
                                                        ▼
                                          ┌──────────┐   ┌──────────────┐
                                          │FINALIZE  │──▶│PROC.SUMMARY │
                                          │(Stage5)  │   │  (Stage6)    │
                                          └──────────┘   └──────────────┘
```

### 6 个 IRON RULE

1. 编排器不越权（只调度不写）
2. MANDATORY 检查点不可跳过
3. 完整性检查(2.5/4.5)必须通过
4. AI 失败模式清单阻断
5. 修订收敛停止（delta<3+无P0）
6. 用户可暂停，不可跳完整性

---

## 7 种入口模式

| 场景 | 输入 | 入口阶段 | 推荐模式路径 |
|------|------|----------|-------------|
| 从头开始 | 无材料 | Stage 1 | socratic→plan→guided→... |
| 有研究数据 | 数据/文献 | Stage 2 | full→plan→... |
| 有论文草稿 | 草稿文件 | Stage 2.5 | integrity→full review→... |
| 有审稿意见 | 审稿反馈 | Stage 4 | revision→re-review→... |
| 已有文献综述 | 综述文档 | Stage 2 | plan→... |
| 只需要格式化 | 定稿文件 | Stage 5 | format-convert |
| 只需要过程记录 | 完成全流程 | Stage 6 | auto |

---

## 文件结构

```
academic-pipeline/
├── SKILL.md                    # 核心入口定义（触发+架构+规则+索引）
├── README.md                   # 本文件——安装+架构+对比+致谢
│
├── agents/                     # 4 个 agent 定义
│   ├── pipeline_orchestrator_agent.md
│   ├── state_tracker_agent.md
│   ├── integrity_verification_agent.md
│   └── collaboration_depth_agent.md
│
├── references/                 # 14 个协议/模板参考文件
│   ├── pipeline_state_machine.md
│   ├── integrity_review_protocol.md
│   ├── ai_research_failure_modes.md
│   ├── two_stage_review_protocol.md
│   ├── external_review_protocol.md
│   ├── process_summary_protocol.md
│   ├── reproducibility_audit.md
│   ├── reinforcement_content.md
│   ├── progress_dashboard_template.md
│   ├── mode_advisor.md
│   ├── team_collaboration_protocol.md
│   ├── plagiarism_detection_protocol.md
│   ├── claim_verification_protocol.md
│   └── ... (更多)
│
├── shared/                     # 共享量规/合约
│   ├── collaboration_depth_rubric.md
│   ├── quality_gates_contract.json
│   └── pipeline_state_contract.json
│
├── templates/                  # 输出模板
│   └── pipeline_status_template.md
│
├── examples/                   # 示例对话日志
│   ├── full_pipeline_example.md
│   └── mid_entry_example.md
│
├── contracts/                  # 合约 schema
│   ├── quality_gates_contract.json
│   ├── pipeline_state_contract.json
│   └── handoff_contract.json
│
├── test-prompts.json           # 测试 prompt 集
├── results.tsv                 # 验证结果记录
└── optimization-report.md      # Darwin 优化记录
```

---

## 与相关 Skill 的关系

```
                    ┌─────────────────────┐
                    │  academic-pipeline  │ ← 编排器（本 Skill）
                    │   (调度+协调+追踪)   │
                    └─────────────────────┘
                              │ 调度
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐
    │deep-research│    │academic-  │      │academic-  │
    │  (Stage1)  │    │paper      │      │paper-     │
    │            │    │(Stg2/4/5) │      │reviewer   │
    └────────────┘    └───────────┘      │(Stg3/3') │
                                          └──────────┘
```

| 对比维度 | academic-pipeline | academic-paper | academic-paper-reviewer | deep-research |
|----------|-------------------|----------------|------------------------|---------------|
| 定位 | 全流程编排器 | 单阶段写作 | 单阶段评审 | 单阶段研究 |
| 覆盖范围 | 10 阶段 | 1 阶段(写作) | 1 阶段(评审) | 1 阶段(研究) |
| 是否独立使用 | 需依赖其他 3 个 Skill | 可独立 | 可独立 | 可独立 |
| 输出 | 全流程过程记录 | 论文草稿 | 评审报告 | 研究报告 |
| 适用场景 | 从头到尾的完整论文项目 | 只需写/修订论文 | 只需评审论文 | 只需做研究 |

---

## 与上游 ARS 的差异

| 功能 | 上游 ARS (CC多agent) | 本 WB 版 (单agent) |
|------|---------------------|--------------------|
| 执行架构 | 多 agent 自动调度 | AI 按阶段手动读取 agent 文件 |
| 检查点 | 自动推进（可配置） | 每阶段必须用户确认 |
| 跨模型 | 支持 ARS_CROSS_MODEL | 需用户手动切换模型 |
| 输出格式 | 多格式自动转换 | Pandoc 可用时转 DOCX；LaTeX→PDF(tectonic) |
| 完整性门控 | 3 轮上限 | 同，但每轮必须用户确认 |
| 失败模式阻断 | 阻断+覆盖 | 阻断+覆盖（需记录推理） |

---

## 许可

CC-BY-NC-4.0 — 原始作品版权归 Cheng-I Wu；WB 适配改动按相同许可发布。

---

## 致谢

- **Cheng-I Wu** — 原始 academic-research-skills v3.7.0 的设计和实现
- **上游仓库** — https://github.com/Imbad0202/academic-research-skills
- **Lu et al. (2026)** — AI 研究失败模式分类法（Nature 651）
- **Wang & Zhang (2026)** — 协作深度量规（IJETHE 23:11）
