# workbuddy-skills

WorkBuddy AI Skill 技能集合 — 学术研究、方法论框架、Skill打磨工坊。

## Skills 列表

| Skill | 描述 | 版本 |
|-------|------|------|
| **academic-pipeline** | 完整学术研究到论文发表流水线（10阶段状态机 + 完整性门控 + 两阶段评审），7种模式 | v4.0.0 |
| **career-41-theories** | 职业生涯研究理论选择推荐（41个理论，6大类覆盖） | v1.0 |
| **lca-lpa-transition-framework** | LCA/LPA/LTA/GMM 全流程方法论引擎 | v1.0 |
| **luban-skill** | Skill打磨工坊 — 把"能用的Skill"打磨成"能被理解、安装、传播、验证、进化"的公共资产 | v1.0 |

## 安装方式

将对应 Skill 文件夹复制到 `~/.workbuddy/skills/` 目录下即可：

```bash
# 示例：安装 academic-pipeline
cp -r academic-pipeline ~/.workbuddy/skills/
```

重启 WorkBuddy 后即可使用，触发词参见各 Skill 的 SKILL.md。

## 学术-pipeline 特别说明

`academic-pipeline` 是本仓库的核心 Skill，提供从研究选题到论文发表的端到端流水线：

- **7 种模式**：full / quick / revision / revision-coach / abstract / lit-review / format-convert
- **10 阶段状态机**：选题 → 文献 → 设计 → 数据 → 分析 → 撰写 → 评审 → 修订 → 格式 → 发布
- **完整性门控**：每个阶段有 MANDATORY 检查点
- **两阶段评审**：内部评审 + 外部评审协议

触发词：学术流水线、研究到论文、学术论文、paper pipeline

## 致谢

- academic-pipeline 上游项目：[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (ARS)
- career-41-theories 基于职业生涯研究理论体系
- luban-skill 参考自花叔的 Skill 打磨方法论
