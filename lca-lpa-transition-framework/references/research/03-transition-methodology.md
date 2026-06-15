# 转换研究（Transition Analysis）方法论文献

## 一、理论基础

### 1.1 核心概念

**转换研究**（Transition / Longitudinal Mixture Modeling）旨在追踪个体在**多个时间点**上的**类别归属变化**，回答"个体如何随时间转移？"这一动态问题。

### 1.2 核心方法体系

| 方法 | 全称 | 适用场景 | 观测变量 |
|------|------|----------|----------|
| **LTA** | Latent Transition Analysis | 类别型潜在变量 | 分类/有序 |
| **GMM** | Growth Mixture Modeling | 连续型潜在变量 | 连续 |
| **LCGA** | Latent Class Growth Analysis | 群体轨迹，类内同质 | 连续 |

### 1.3 三大方法的选择决策树

```
开始
  │
  ├── 时间点数量
  │   ├── 2个时间点 → LTA（首选）
  │   └── ≥3个时间点 → 进入下一步
  │
  ├── 潜在变量类型
  │   ├── 类别型 → LTA
  │   └── 连续型 → GMM / LCGA
  │
  └── 类内变异假设
      ├── 类内同质 → LCGA
      └── 类内异质 → GMM
```

---

## 二、潜类别转换分析（LTA）

### 2.1 核心原理

LTA是LCA在纵向数据上的扩展，追踪个体在T个时间点的潜在类别归属，并估计**转换概率矩阵**。

**数学形式**：
$$P(Y_{t1}, Y_{t2}, ..., Y_{tT}) = \sum_{c1} \sum_{c2} ... \sum_{cT} \pi_{c1} \omega_{c2|c1} ... \omega_{cT|c(T-1)} \prod_{t=1}^{T} P(Y_t | c_t)$$

其中：
- $\pi_{c1}$：初始类别概率
- $\omega_{c'|c}$：从类别c转换到类别c'的转换概率

### 2.2 转换概率矩阵

**示例（3类别，2时间点）**：

|  | 类别1 (T2) | 类别2 (T2) | 类别3 (T2) |
|--|-----------|-----------|-----------|
| **类别1 (T1)** | 0.70 | 0.20 | 0.10 |
| **类别2 (T1)** | 0.15 | 0.60 | 0.25 |
| **类别3 (T1)** | 0.10 | 0.30 | 0.60 |

**解读**：
- 对角线元素（0.70, 0.60, 0.60）：保持原类别的"驻留概率"
- 非对角线元素：从某类别转换到其他类别的概率

### 2.3 Mplus实现

```mplus
TITLE: Latent Transition Analysis;
DATA: FILE = longitudinal_data.csv;
VARIABLE: NAMES = y1_t1-y5_t1 y1_t2-y5_t2;
          CATEGORICAL = y1_t1-y5_t1 y1_t2-y5_t2;
          CLASSES = c1(3) c2(3);  ! 两个时间点，各3类别
ANALYSIS: TYPE = MIXTURE;
          ESTIMATOR = MLR;
          STARTS = 200 50;
MODEL: %OVERALL%
  ! 初始类别模型（T1）
  c1 BY y1_t1-y5_t1;
  ! 转换模型（T2）
  c2 BY y1_t2-y5_t2;
  c2 ON c1;  ! 关键：c1预测c2
OUTPUT: TECH1 TECH8;
```

### 2.4 测量等值性检验（LTA）

**必要性**：跨时间点比较类别归属时，必须先验证测量等值性。

**检验序列**：
```
Step 1: Configural（形态等值）
        → 所有时间点类别结构相同
        
Step 2: Strong（强等值）
        → 条件概率跨时间点相等
        
Step 3: 检验转换概率是否显著
```

---

## 三、增长混合模型（GMM）

### 3.1 核心原理

GMM假设个体发展轨迹来自**不同潜在类别**的混合，每个类别有其独特的发展参数（截距、斜率）。

**数学形式**：
$$Y_{ti} = \pi_{0i} + \pi_{1i} \cdot Time_{ti} + \epsilon_{ti}$$

其中：
- $\pi_{0i}$：个体i的初始状态（截距）
- $\pi_{1i}$：个体i的发展速率（斜率）
- $\epsilon_{ti}$：残差

### 3.2 GMM vs LCGA

| 特征 | GMM | LCGA |
|------|-----|------|
| 类内变异 | 允许 | 不允许 |
| 估计参数 | 更多 | 更少 |
| 模型复杂性 | 高 | 低 |
| 小样本稳定性 | 较低 | 较高 |
| 灵活性 | 高 | 低 |

**推荐**：
- 大样本（≥500）且理论支持时 → GMM
- 小样本或类内同质假设合理时 → LCGA

### 3.3 Mplus实现

```mplus
TITLE: Growth Mixture Modeling;
DATA: FILE = gmm_data.csv;
VARIABLE: NAMES = y_t1-y_t4 time;
          MISSING = ALL (-999);
          CLASSES = c(3);  ! 3个增长轨迹类别
ANALYSIS: TYPE = MIXTURE;
          ESTIMATOR = MLR;
          STARTS = 200 50;
MODEL: %OVERALL%
  ! 潜在发展变量
  i BY y_t1@1 y_t2@1 y_t3@1 y_t4@1;  ! 截距
  s BY y_t1@0 y_t2@1 y_t3@2 y_t4@3;  ! 斜率（线性）

  ! 各类别发展参数
  %c#1%
    i s;  ! 允许变异
    [i s];  ! 各类别均值
  %c#2%
    i s;
    [i s];
  %c#3%
    i s;
    [i s];
OUTPUT: TECH1 TECH8;
PLOT: TYPE = PLOT3;
      SERIES = y_t1-y_t4(s);
```

### 3.4 模型选择标准

| 指标 | 判别标准 | 特别说明 |
|------|----------|----------|
| BIC | 越小越好 | 首选指标 |
| Entropy | ≥ 0.80 | 分类质量 |
| LMR-LRT | p < 0.05 | 显著性检验 |
| BLRT | p < 0.05 | Bootstrap检验 |
| 类别轨迹可解释性 | 理论支撑 | 必要条件 |

---

## 四、软件实现对比

### 4.1 Mplus（综合推荐）

**LTA完整语法**：
```mplus
TITLE: LTA with Covariates and Distal Outcomes;
DATA: FILE = data.dat;
VARIABLE: NAMES = y1-y5_t1 y1-y5_t2 y1-y5_t3;
          CATEGORICAL = y1-y5_t1 y1-y5_t2 y1-y5_t3;
          CLASSES = c1(3) c2(3) c3(3);
          AUXILIARY = x1-x3 (R3STEP);  ! 预测变量
          IDVARIABLE = id;
ANALYSIS: TYPE = MIXTURE;
          ESTIMATOR = MLR;
MODEL: %OVERALL%
  c1 BY y1-y5_t1;
  c2 BY y1-y5_t2;
  c3 BY y1-y5_t3;
  c2 ON c1;
  c3 ON c2;
OUTPUT: TECH1 TECH8 TECH14;
SAVEDATA: FILE = lta_results.csv;
          SAVE = CPROB;
```

### 4.2 R实现（latentnet / depigner）

```r
library(depigner)

# LTA实现
lta_model <- lta(
  data = my_data,
  n_classes = c(3, 3),  # T1=3类, T2=3类
  items = list(
    t1 = c("y1_t1", "y2_t1", "y3_t1"),
    t2 = c("y1_t2", "y2_t2", "y3_t2")
  )
)
```

---

## 五、外生变量与结果变量整合

### 5.1 预测变量（前因变量）

**R3STEP方法**（推荐）：
```mplus
VARIABLE: AUXILIARY = cov1 cov2 (R3STEP);
```

**DCAT方法**（分类预测）：
```mplus
VARIABLE: AUXILIARY = cov1 cov2 (DCAT);
```

### 5.2 结果变量（ distal outcomes）

**BCH方法**（推荐）：
```mplus
VARIABLE: AUXILIARY = outcome (BCH);
```

### 5.3 三步法完整流程

```
Step 1: 确定时间点1的最优类别数
        ↓
Step 2: 确定时间点2的最优类别数
        ↓
Step 3: 估计转换概率矩阵
        ↓
Step 4: 纳入外生变量预测转换
        ↓
Step 5: 检验结果变量差异
```

---

## 六、在HR/教育/心理领域的应用

### 6.1 典型研究问题

| 领域 | 研究问题 | 方法选择 |
|------|----------|----------|
| HR管理 | 员工敬业度如何随时间变化？ | GMM |
| 组织行为 | 工作压力类别如何转换？ | LTA |
| 教育研究 | 学习者策略轨迹有几类？ | LCGA |
| 心理健康 | 心理弹性发展轨迹分类？ | GMM |
| 职业发展 | 职业认同如何转换？ | LTA |

### 6.2 经典文献

1. **Collins & Lanza (2010)** - 《Latent Class and Latent Transition Analysis》纵向LCA权威著作
2. **Jung & Wickrama (2008)** - GMM入门与应用
3. **Muthén & Muthén (2000)** - Mplus混合建模发展
4. **Nylund-Gibson et al.** - GMM模型选择模拟研究

---

## 七、方法论注意事项

### 7.1 时间点设计

- **最少时间点**：LTA需要≥2个，理想≥3个
- **时间间隔**：应与理论框架匹配
- **测量时机**：避免回忆偏差

### 7.2 样本量要求

| 方法 | 最低样本 | 推荐样本 |
|------|----------|----------|
| LTA | 200-300 | 500+ |
| GMM | 300-500 | 1000+ |
| LCGA | 200-300 | 500+ |

### 7.3 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 模型不收敛 | 类别过多/参数过多 | 减少类别 |
| 转换概率不稳定 | 稀有转换路径 | 合并类别 |
| 类内变异估计失败 | GMM过于复杂 | 改用LCGA |
| 时间间隔不等 | 数据结构问题 | 设定不等间距 |

---

## 八、论文结果报告模板

```markdown
### 潜在类别转换分析

#### 模型选择

| 模型 | BIC | Entropy | 类别比例T1 | 类别比例T2 |
|------|-----|---------|-----------|-----------|
| 2-2类 | xxx | 0.92 | 45%/55% | 50%/50% |
| 3-3类 | xxx | 0.87 | 30%/35%/35% | 28%/38%/34% |

#### 测量等值性

采用卡方差异检验验证测量等值性。结果显示弱等值性假设成立（Δχ² = xx, p = xx），
可进行跨时间点的类别比较。

#### 转换概率矩阵

|          | 类别1(T2) | 类别2(T2) | 类别3(T2) |
|----------|-----------|-----------|-----------|
| 类别1(T1) | 0.72      | 0.18      | 0.10      |
| 类别2(T1) | 0.15      | 0.65      | 0.20      |
| 类别3(T1) | 0.12      | 0.25      | 0.63      |

#### 转换模式解读

[基于转换概率矩阵进行理论解读，描述主要转换路径]
```

---

*转换研究核心：从"截面异质性"走向"动态发展轨迹"*
