import pathlib

p = pathlib.Path('C:/Users/songh/.workbuddy/skills/career-41-theories/SKILL.md')
lines = p.read_text(encoding='utf-8').split('\n')
print(f'Total lines: {len(lines)}')

# ===== Round 4 part 2: 在Step 3模板中加入具体示例 =====
# 找到Step 3的"研究方法适配卡"模板的结束位置，然后加入"✅ 完整卡片示例"
step3_start = None
for i, line in enumerate(lines):
    if '### Step 3' in line:
        step3_start = i
        break

# 找到Step 3输出格式模板的结束位置（下一个"**输出**："或"**失败模式**："）
template_end3 = None
for i in range(step3_start, min(step3_start+80, len(lines)):
    if '**输出**：' in lines[i] and i > step3_start + 10:
        template_end3 = i
        break

print(f'Step 3 输出位置: line {template_end3+1}')

# 在 template_end3 之前插入"✅ 完整卡片示例"
example_3 = '''
> ✅ **完整卡片示例**（基于SCCT）：
> 
> #### 社会认知职业理论(SCCT) 研究方法适配卡
> 
> | 维度 | 具体内容 |
> |------|---------|
> | 推荐研究设计 | 量化；横截面（大样本）或纵向（3波） |
> | 典型测量工具 | 职业决策自我效能感量表（Betz & Hackett, 1983）<br>中文版：龙立荣等（2002）开发 |
> | IV建议 | 1. 职业决策自我效能感  2. 结果预期 |
> | DV建议 | 1. 职业选择意向  2. 职业决策困难得分 |
> | Mediator建议 | 1. 职业探索行为  2. 社会支持感知 |
> | Moderator建议 | 1. 性别（男=0, 女=1） 2. 父母教育水平 |
> | 样本要求 | 量化：最小N=200（SEM分析）；纵向：每波N≥150 |
> | 数据分析方法 | 相关分析 → 分层回归 → 结构方程模型（SEM） |
'''

if template_end3:
    lines.insert(template_end3, example_3.strip())
    print(f'Inserted Step 3 example at line {template_end3+1}')

# ===== Round 4 part 3: 在Step 4模板中加入具体命题示例 =====
# 找到Step 4的"假设命题"模板的结束位置
step4_start = None
for i, line in enumerate(lines):
    if '### Step 4' in line:
        step4_start = i
        break()

print(f'Step 4 starts at line {step4_start+1}')

# 找到Step 4输出格式模板的结束位置
template_end4 = None
for i in range(step4_start, min(step4_start+80, len(lines))):
    if '**输出**：' in lines[i] and i > step4_start + 10:
        template_end4 = i
        break()

print(f'Step 4 输出位置: line {template_end4+1}')

# 在 template_end4 之前插入"✅ 好的命题示例"
example_4 = '''
> ✅ **好的命题示例**（基于SCCT）：
> 
> ### 假设命题组（基于社会认知职业理论）
> 
> #### 主理论：社会认知职业理论(SCCT)
> - H1: 职业决策自我效能感 正向预测 职业选择意向（理论来源：Lent et al., 1994）
> - H2: 结果预期 中介 职业决策自我效能感 与 职业选择意向 的关系（理论来源：Lent et al., 1994）
> - H3: 性别 调节 职业决策自我效能感 与 职业选择意向 的关系——当性别=女性时，职业决策自我效能感对职业选择意向的影响更强（理论来源：Lent et al., 1994；中国情境调节效应待验证）
> 
> #### 备选理论：生涯建构理论(CCT)
> - H1: 生涯适应力（4C） 正向预测 职业探索行为（理论来源：Savickas, 2005）
> - H2: 职业呼唤 中介 生涯适应力 与 职业探索行为 的关系（理论来源：Savickas, 2005；Duffy et al., 2012）
'''

if template_end4:
    lines.insert(template_end4, example_4.strip())
    print(f'Inserted Step 4 example at line {template_end4+1}')

# 写回文件
p.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nRound 4 optimization (part 2 & 3) done.')
print(f'Final line count: {len(lines)}')
