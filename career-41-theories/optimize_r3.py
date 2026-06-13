import pathlib

p = pathlib.Path('C:/Users/songh/.workbuddy/skills/career-41-theories/SKILL.md')
lines = p.read_text(encoding='utf-8').split('\n')
print(f'Total lines: {len(lines)}')

# ===== 优化Step 2操作指令（提升dim5和dim6）=====
step2_start = None
for i, line in enumerate(lines):
    if '### Step 2' in line:
        step2_start = i
        break

op2_idx = None
for i in range(step2_start, min(step2_start+30, len(lines))):
    if '**操作**：' in lines[i]:
        op2_idx = i
        break

print(f'Step 2 操作 at line {op2_idx+1}')

# 找到"**决策树规则**："或"**输出**："的位置
tree_idx = None
for i in range(op2_idx, min(op2_idx+40, len(lines))):
    if '**决策树规则**：' in lines[i] or '**输出**：' in lines[i]:
        tree_idx = i
        break

print(f'Step 2 决策树规则/输出 at line {tree_idx+1}')

new_op2 = '''**操作**：
1. 查「理论选择决策树」（见附录A）匹配候选理论
2. 至少推荐2个理论（主理论+备选理论）
3. **读取对应文件获取完整6维度内容**（按以下映射）：
   - 理论#1-#5  → 读取 `references/research/01-matching-theories.md`
   - 理论#6-#12 → 读取 `references/research/02-development-theories.md`
   - 理论#13-#17 → 读取 `references/research/03-decision-theories.md`
   - 理论#18-#28 → 读取 `references/research/04-05-organization-motivation-theories.md`
   - 理论#29-#34 → 读取 `references/research/06-system-theories.md`
   - 理论#35-#41 → 读取 `references/research/07-construction-boundaryless-theories.md`
4. 每个理论输出：
   - **匹配理由**：为什么适合这个问题（引用决策树规则）
   - **核心命题**（可操作化）：从该理论提取的可直接写成假设命题的句子
   - **研究方法适配摘要**：设计类型 + 典型测量工具（量表名+作者+年份）

**输出格式**：
```
### 推荐理论
1. **[理论名]**（匹配度：高/中/低）
   - 匹配理由：[具体理由]
   - 核心命题：[可操作化的命题，可直接写成H1]
   - 研究方法适配：[设计类型]；测量工具：[具体量表]
   
2. **[备选理论名]**（匹配度：中/低）
   - 匹配理由：...
   - 核心命题：...
   - 研究方法适配：...
```'''

if op2_idx and tree_idx:
    lines[op2_idx:tree_idx] = new_op2.split('\n')
    print(f'Replaced Step 2 操作 with more specific instructions')
    print(f'New total lines: {len(lines)}')

# ===== 优化Step 3操作指令（提升dim5）=====
step3_start = None
for i, line in enumerate(lines):
    if '### Step 3' in line:
        step3_start = i
        break

op3_idx = None
for i in range(step3_start, min(step3_start+30, len(lines))):
    if '**操作**：' in lines[i]:
        op3_idx = i
        break

print(f'Step 3 操作 at line {op3_idx+1}')

# 找到"**输出**："或"**失败模式**："的位置
out3_idx = None
for i in range(op3_idx, min(op3_idx+40, len(lines))):
    if '**输出**：' in lines[i] or '**失败模式**：' in lines[i]:
        out3_idx = i
        break

print(f'Step 3 输出/失败模式 at line {out3_idx+1}')

new_op3 = '''**操作**：
对每个候选理论：
1. **读取对应文件**（映射见Step 2）中的"研究方法适配"章节
2. 提取以下信息，填入「研究方法适配卡」：
   - **推荐研究设计**：量化/质性/混合；横截面/纵向/ESM/实验
   - **典型测量工具**：量表名称 + 作者 + 年份；中文版开发情况（已开发/需自行翻译）
   - **变量设计建议**：IV/DV/Mediator/Modifier 各推荐2-3个具体变量名
   - **样本要求**：量化设计的最小样本量（根据推荐统计方法）；质性设计的建议样本量（n=？）
   - **数据分析方法**：相关/回归/SEM/多层模型/主题分析/...

**输出格式**（每个候选理论一张卡）：
```
#### [理论名] 研究方法适配卡

| 维度 | 具体内容 |
|------|---------|
| 推荐研究设计 | [量化/质性/混合]；[横截面/纵向/ESM/实验] |
| 典型测量工具 | [量表名]（[作者]，[年份]）<br>中文版：[已开发/需自行翻译] |
| IV建议 | 1. [具体变量名] 2. [具体变量名] |
| DV建议 | 1. [具体变量名] 2. [具体变量名] |
| Mediator建议 | 1. [具体变量名] 2. [具体变量名] |
| Moderator建议 | 1. [具体变量名（调节变量）] 2. [具体变量名] |
| 样本要求 | 量化：最小N=[具体数字]；质性：建议n=[具体数字] |
| 数据分析方法 | [相关/回归/SEM/多层模型/主题分析/...] |
```'''

if op3_idx and out3_idx:
    lines[op3_idx:out3_idx] = new_op3.split('\n')
    print(f'Replaced Step 3 操作 with more specific template')
    print(f'New total lines: {len(lines)}')

# 写回文件
p.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nRound 3 optimization done. Final line count: {len(lines)}')
