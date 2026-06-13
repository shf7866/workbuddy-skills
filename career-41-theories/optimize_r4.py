import pathlib

p = pathlib.Path('C:/Users/songh/.workbuddy/skills/career-41-theories/SKILL.md')
lines = p.read_text(encoding='utf-8').split('\n')
print(f'Total lines: {len(lines)}')

# ===== Round 4: 提升dim5（更具体的操作指令）=====

# 修改1：在Step 2操作指令中加入"语义匹配"指令
# 找到Step 2的"操作"部分
step2_start = None
for i, line in enumerate(lines):
    if '### Step 2' in line:
        step2_start = i
        break

op2_idx = None
for i in range(step2_start, min(step2_start+40, len(lines))):
    if '**操作**：' in lines[i]:
        op2_idx = i
        break

print(f'Step 2 操作 at line {op2_idx+1}')

# 在操作指令的第1条之后插入"语义匹配"指令
# 当前操作指令是：
# 1. 查「理论选择决策树」（见附录A）匹配候选理论
# 2. 至少推荐2个理论（主理论+备选理论）
# 3. 读取对应文件获取完整6维度内容
# 4. 每个理论输出：匹配理由/核心命题/研究方法适配摘要

# 在第1条之后插入新的第2条（语义匹配），后面的编号顺延
# 先找到第1条的结束位置（下一个数字编号，或"**输出格式**："）
insert_pos = None
for i in range(op2_idx+1, min(op2_idx+20, len(lines))):
    if lines[i].strip().startswith('2. '):
        insert_pos = i
        break

print(f'Insert "语义匹配" instruction at line {insert_pos+1}')

semantic_match = '''2. 【语义匹配】如果决策树无法精确匹配，根据理论核心命题与用户问题的语义相似度，推荐最相关的2-3个理论
   - 计算方法：比对用户问题中的关键词与理论核心命题中的关键词（见附录C或对应文件）
   - 优先推荐核心命题可直接操作化为假设命题的理论
3. 至少推荐2个理论（主理论+备选理论）
4. 读取对应文件获取完整6维度内容
5. 每个理论输出：匹配理由/核心命题/研究方法适配摘要'''

# 替换原来的第2-4条
# 原来是第2条=推荐2个理论，第3条=读取文件，第4条=每个理论输出
# 现在改成：第2条=语义匹配，第3条=推荐2个理论，第4条=读取文件，第5条=每个理论输出
# 所以需要替换从"2. 至少推荐2个理论"开始，到"**输出格式**："之前的内容

# 找到"**输出格式**："的位置
out_fmt_idx = None
for i in range(insert_pos, min(insert_pos+30, len(lines))):
    if '**输出格式**：' in lines[i]:
        out_fmt_idx = i
        break

print(f'"**输出格式**：" at line {out_fmt_idx+1}')

if insert_pos and out_fmt_idx:
    # 替换 lines[insert_pos:out_fmt_idx] 为 new content
    lines[insert_pos:out_fmt_idx] = semantic_match.split('\n')
    print(f'Inserted semantic matching instruction')
    print(f'New total lines: {len(lines)}')

# 写回文件
p.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nRound 4 optimization (part 1) done.')
