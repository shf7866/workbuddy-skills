import pathlib

p = pathlib.Path('C:/Users/songh/.workbuddy/skills/career-41-theories/SKILL.md')
lines = p.read_text(encoding='utf-8').split('\n')
print(f'Total lines: {len(lines)}')

# ===== Round 5: 提升dim6（更明确的文件读取指引）=====
# 修改Step 2的操作指令，加入更具体的文件读取指引
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

# 在操作指令中，把"读取对应文件获取完整6维度内容"改成更具体的指令
# 找到"读取对应文件获取完整6维度内容"的行
read_idx = None
for i in range(op2_idx, min(op2_idx+30, len(lines))):
    if '读取对应文件' in lines[i] or '获取完整6维度' in lines[i]:
        read_idx = i
        break

print(f'"读取对应文件" at line {read_idx+1}')

if read_idx:
    # 替换成更具体的指令
    lines[read_idx] = '3. **读取对应文件获取完整6维度内容**（按以下映射，搜索 `## [理论名]` 章节）：'
    # 在第4条（原来的"4. 每个理论输出："之前插入更具体的读取指引
    # 找到"4. 每个理论输出："的行
    output_idx = None
    for i in range(read_idx, min(read_idx+30, len(lines))):
        if '4. 每个理论输出' in lines[i] or '每个理论输出' in lines[i]:
            output_idx = i
            break
    
    print(f'"每个理论输出" at line {output_idx+1}')

    if output_idx:
        # 插入更具体的读取指引
        read_guide = '''> **具体读取指引**：
> - 读取文件后，搜索 `## [理论名]` 章节（如 `## 1. 人—职匹配理论`）
> - 提取该章节下的6个二级标题：核心概念/研究方法适配/实践应用/当代青年指引/理论局限与争议/关键文献
> - 如果文件内容过长（>1000字），先输出核心概念+研究方法适配，询问用户是否需要展开其他部分
> 
> **文件与理论映射**（精确搜索关键词）：
> - 理论#1-#5：搜索 `## 1.` / `## 2.` / `## 3.` / `## 4.` / `## 5.`
> - 理论#6-#12：搜索 `## 6.` / `## 7.` / ... / `## 12.`
> - 理论#13-#17：搜索 `## 13.` / ... / `## 17.`
> - 理论#18-#28：搜索 `## 18.` / ... / `## 28.`
> - 理论#29-#34：搜索 `## 29.` / ... / `## 34.`
> - 理论#35-#41：搜索 `## 35.` / ... / `## 41.`
> 
> 如果搜索不到确切章节，读取文件开头部分（前200行），根据章节标题手动定位。'''

        lines.insert(output_idx, read_guide)
        print(f'Inserted specific read guide at line {output_idx+1}')

# ===== Round 5 part 2: 提升dim9（更具体的危险动作）=====
# 找到"**危险动作**（未经用户确认，不得执行）："章节
danger_idx = None
for i, line in enumerate(lines):
    if '**危险动作**' in line:
        danger_idx = i
        break

print(f'"危险动作" at line {danger_idx+1}')

if danger_idx:
    # 在"危险动作"章节中，加入更具体的条款
    # 找到"**不要做的事**："的行
    no_do_idx = None
    for i in range(danger_idx, min(danger_idx+30, len(lines))):
        if '**不要做的事**：' in lines[i]:
            no_do_idx = i
            break

    print(f'"不要做的事" at line {no_do_idx+1}')

    if no_do_idx:
        # 在 "不要做的事" 之前插入更具体的危险动作条款
        new_danger = '''**危险动作**（未经确认不得执行）：
1. 不要在未经🔴 CHECKPOINT确认的情况下，直接输出完整假设命题组（>500字）
2. 不要在未经用户同意的情况下，自动读取 `references/research/` 下的大段内容（>1000字）并输出
3. 不要假设用户已经了解某个理论，每次推荐都要给出匹配理由和核心命题摘要（≤200字）
4. 不要在用户说"只要理论名称"时，仍然输出完整6维度内容（>1000字）
5. 不要跳过Step 1的问题结构化，直接跳到理论推荐
6. 不要在输出内容超过1500字时，不分段直接输出——必须分段（先给核心部分，再询问是否需要展开）
7. 不要在未经用户请求的情况下，自动生成PDF/Word/DOCX等文件——只生成Markdown格式

'''

        # 替换原来的"危险动作"章节（从 danger_idx 到 no_do_idx 之前）
        lines[danger_idx:no_do_idx] = new_danger.split('\n')

        print(f'Replaced "危险动作" with more specific clauses')

# 写回文件
p.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nRound 5 optimization done. Final line count: {len(lines)}')
