---
name: academic-pipeline
version: 4.0.0
description: |
  Complete academic research-to-publication pipeline orchestrator.
  10 stages, mandatory integrity checks, two-stage peer review, reproducible quality gating.
  Trigger words: 学术流水线, 研究到论文, 完整论文流程, 端到端论文, 研究到发表, 学术论文,
  academic pipeline, research to paper, full paper workflow, end-to-end paper, paper pipeline.
license: CC-BY-NC-4.0
compatibility: workbuddy claude-code cursor windsurf openclaw hermes gemini-cli opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Skill
  - TaskCreate
  - TaskUpdate
  - TaskList
---

# Academic Pipeline v4.0.0 — 学术研究→发表全流程编排器

> 基于 Cheng-I Wu 的 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v3.7.0 改编，
> 适配 WorkBuddy 单 agent 执行架构。agent 文件保留在 `agents/` 目录供 AI 按阶段读取。
> **编排器不执行实质性工作——只检测阶段、推荐模式、调度 skill、管理转换、跟踪状态。**

---

## 触发条件

**中文触发词**：学术流水线、研究到论文、完整论文流程、论文流水线、端到端论文、研究到发表、学术论文
**英文触发词**：academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow

**不触发场景**：

| 场景 | 应使用 |
|------|--------|
| 只搜索资料/文献综述 | `deep-research` |
| 只写论文（无需研究阶段） | `academic-paper` |
| 只评审论文 | `academic-paper-reviewer` |
| 只检查引用格式 | `academic-paper`（citation-check） |
| 只转换论文格式 | `academic-paper`（format-convert） |

> 流水线是 opt-in，不是强制入口。用户已在用特定 skill 时，尊重该入口。

---

## 快速开始

| 场景 | 输入示例 | 入口阶段 |
|------|----------|----------|
| 从头开始 | "我想写一篇关于 AI 对高等教育影响的论文" | Stage 1（RESEARCH） |
| 已有论文 | "我已经有论文了，帮我评审" | Stage 2.5（INTEGRITY） |
| 收到审稿意见 | "我收到了审稿意见，帮我修订" | Stage 4（REVISE） |
| 已有文献综述 | "我现在只有文献综述，接下来做什么" | Stage 2（WRITE） |

---

## 流水线架构（10 阶段）

| # | 阶段 | 调度 | 模式 | 交付物 |
|---|------|------|------|--------|
| 1 | RESEARCH | `deep-research` | socratic / full / quick | RQ Brief + Bibliography + Synthesis |
| 2 | WRITE | `academic-paper` | plan / full | Paper Draft |
| **2.5** | **INTEGRITY** | integrity_agent | pre-review | 完整性验证报告 + 修正后论文 |
| 3 | REVIEW | `academic-paper-reviewer` | full | 5 份评审 + 编辑决定 + 修订路线图 |
| 4 | REVISE | `academic-paper` | revision | Revised Draft + Response to Reviewers |
| **3'** | **RE-REVIEW** | `academic-paper-reviewer` | re-review | 验证评审报告 + 残留问题 |
| **4'** | **RE-REVISE** | `academic-paper` | revision | 第二轮修订稿 |
| **4.5** | **FINAL INTEGRITY** | integrity_agent | final-check | 最终验证报告（必须零问题通过） |
| 5 | FINALIZE | `academic-paper` | format-convert | 最终论文（MD / DOCX / LaTeX / PDF） |
| 6 | PROCESS SUMMARY | 编排器自身 | auto | 过程记录 MD + PDF（双语） |

### 状态机

```
1 → 确认 → 2 → 确认 → 2.5 → PASS → 3 / FAIL→修复(≤3轮) → 2
3 → Accept→4.5 / Minor|Major→4 / Reject→2或结束
4 → 确认 → 3' → Accept|Minor→4.5 / Major→4'
4' → 确认 → 4.5（不再回评审）
4.5 → PASS(零问题)→5 / FAIL→修复(≤3轮)
5 → MD→DOCX→LaTeX→PDF → 6
6 → 过程记录 → 结束
```

> 完整定义见 `references/pipeline_state_machine.md`

---

## 核心规则（IRON RULES）

| # | 规则 | 含义 |
|---|------|------|
| 1 | **编排器不越权** | 只调度协调，不写内容/不做评审 |
| 2 | **MANDATORY 检查点不可跳过** | 完整性边界(2.5/4.5)、评审决定(3/3')、最终化前(5) 必须用户明确确认 |
| 3 | **2.5/4.5 完整性检查必须通过** | Stage 4.5 需零问题；独立从头验证，不只复查已知问题 |
| 4 | **失败模式检查清单阻断** | 7 模式 AI 研究失败清单(Stage 2.5+4.5)是 MANDATORY+BLOCKING；覆盖需用户推理记录 |
| 5 | **修订收敛停止** | delta<3 分且无 P0 问题 → 建议停止；硬上限 2 轮(4+4') |
| 6 | **用户可暂停不可跳完整性** | 随时可暂停恢复，但不能绕过 2.5/4.5 |

---

## 检查点系统

每个阶段完成后主动提示用户确认。三级自适应：

| 类型 | 使用时机 | 特征 |
|------|----------|------|
| **FULL** | 首次、完整性边界后、最终化前 | 交付物列表 + 决定仪表板 + 所有选项 |
| **SLIM** | 连续 2+ 次 "continue" 后 | 单行状态 + 继续/暂停提示 |
| **MANDATORY** | 2.5/4.5 FAIL、评审决定、Stage 5 | 不可跳过，需明确输入 |

**自适应规则**：首次→FULL；连续 "continue"→降级 SLIM；4+ 次 continue→强制 FULL；完整性边界→MANDATORY

**自检问题**（每个 FULL 检查点前）：引用完整性？谄媚式让步？质量轨迹≥前阶段？范围纪律？交付物齐全？

> 仪表板模板见 `references/progress_dashboard_template.md`

---

## Anti-Patterns（8 条禁令）

| # | 禁止 | 正确 |
|---|------|------|
| 1 | 跳过完整性检查 | 2.5/4.5 是 MANDATORY |
| 2 | 编排器执行实质工作 | 只调度，不写/不评 |
| 3 | MANDATORY 检查点自动推进 | 必须用户明确确认 |
| 4 | 跨阶段质量降级 | 质量<前阶段→PAUSE 重新加载原则 |
| 5 | 静默丢弃审稿关切 | R&R 表逐条追踪 |
| 6 | 4.5 只复查已知问题 | 必须独立从头验证 |
| 7 | 夸大协作质量分数 | 诚实第一，每分需引用证据 |
| 8 | 绕过失败模式阻断 | 无 --no-block 标志；覆盖需记录推理 |

---

## 协议索引

| 协议 | 文件 | 用途 |
|------|------|------|
| 状态机 | `references/pipeline_state_machine.md` | 所有合法转换、前置条件 |
| 完整性评审 | `references/integrity_review_protocol.md` | 5 阶段引用/主张验证 |
| AI 失败模式 | `references/ai_research_failure_modes.md` | 7 模式检查清单(阻断) |
| 两阶段评审 | `references/two_stage_review_protocol.md` | Stage 3+3' 流程 |
| 外部评审 | `references/external_review_protocol.md` | 人类审稿反馈集成 |
| 过程摘要 | `references/process_summary_protocol.md` | Stage 6 协作质量+自反思 |
| 可重复性 | `references/reproducibility_audit.md` | 审计轨迹格式 |
| 强化内容 | `references/reinforcement_content.md` | 阶段转换强化表 |
| 进度仪表板 | `references/progress_dashboard_template.md` | ASCII 仪表板模板 |
| 模式顾问 | `references/mode_advisor.md` | 用户意图→skill+模式映射 |
| 团队协作 | `references/team_collaboration_protocol.md` | 多人角色/handoff/版本控制 |
| 剽窃检测 | `references/plagiarism_detection_protocol.md` | 原创性+自我剽窃+AI文本 |
| 主张验证 | `references/claim_verification_protocol.md` | 主张提取/来源/交叉引用 |
| 协作深度量规 | `shared/collaboration_depth_rubric.md` | 4 维量规(Wang & Zhang 2026) |

---

## Agent 文件

| Agent | 文件 | 职责 |
|-------|------|------|
| pipeline_orchestrator | `agents/pipeline_orchestrator_agent.md` | 编排决策 |
| state_tracker | `agents/state_tracker_agent.md` | 流水线状态维护 |
| integrity_verification | `agents/integrity_verification_agent.md` | 5 阶段完整性验证 |
| collaboration_depth | `agents/collaboration_depth_agent.md` | 协作深度评估（仅建议，从不阻断） |

---

## 错误恢复

| 阶段 | 错误 | 处理 |
|------|------|------|
| Intake | 无法确定入口 | 询问用户材料和目标 |
| Stage 1 | research 不收敛 | 切换模式或缩小范围 |
| Stage 2 | 缺研究基础 | 建议返回 Stage 1 |
| Stage 2.5 | 3 轮仍 FAIL | 列出不可验证项；用户决定 |
| Stage 3 | Reject | 选项：重构(Stage 2)或放弃 |
| Stage 4 | 修订不完整 | 列出未解决项；确认继续 |
| 任何 | 用户离开 | 保存状态；下次恢复 |
| 任何 | Skill 执行失败 | 重试/暂停/模式切换；不得跳完整性门控 |

---

## 中途进入协议

1. **检测材料** → 识别可用材料和缺口
2. **不能跳过 Stage 2.5** → 有论文必须先完整性验证再评审
3. **唯一例外** → 用户提供先前验证报告且内容未修改

---

## Collaboration Depth Observer（v3.5.0，仅建议）

- **从不阻断**任何检查点进展
- 调用时机：FULL/SLIM 检查点、Stage 6 完成后；**不**在 MANDATORY(2.5/4.5)调用
- 4 维度：Delegation Intensity / Cognitive Vigilance / Cognitive Reallocation / Zone Classification
- 量规：Wang & Zhang (2026) IJETHE 23:11
- 跨模型：分歧>2 分时标记，不静默平均

> 完整程序见 `agents/collaboration_depth_agent.md` + `shared/collaboration_depth_rubric.md`

---

## 版本与致谢

| 项目 | 内容 |
|------|------|
| 上游版本 | academic-research-skills v3.7.0（Cheng-I Wu） |
| WB 适配版 | v4.0.0 |
| 上游仓库 | https://github.com/Imbad0202/academic-research-skills |
| 许可 | CC-BY-NC-4.0 |

---

## 测试验证

### 测试 1：完整流程
```
我想写一篇关于AI对高等教育质量保证影响的学术论文。
```
→ 检测为"从头开始" → Stage 1 → 输出状态面板 → 每阶段确认

### 测试 2：中途进入
```
我已经有论文草稿了，帮我评审一下。
```
→ 检测为"已有论文" → Stage 2.5 → Stage 3

### 测试 3：修订模式
```
我收到了审稿意见，帮我修订论文。
```
→ 检测为"修订" → Stage 4 → Stage 4.5 → Stage 3'

### 通过条件
- ✅ 测试 1-3 均正确检测阶段
- ✅ 调度与架构表一致
- ✅ 每阶段完成后主动提示确认
- ✅ 不自动跳过 MANDATORY 检查点
