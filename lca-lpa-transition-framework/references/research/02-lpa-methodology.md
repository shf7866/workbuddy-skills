# 潜在剖面分析（LPA）方法论文献

## 一、理论基础

### 1.1 核心原理

潜在剖面分析（Latent Profile Analysis, LPA）是一种以**连续潜在变量**刻画**个体差异**的统计分析方法。与LCA不同，LPA的观测变量必须是**连续型指标**，输出的是**剖面中心**和**剖面内变异**。

**数学形式**：
$$P(Y_i | C_i = k) = \prod_{j=1}^{J} \phi(Y_{ij} | \mu_{jk}, \sigma_{jk}^2)$$

其中：
- $\mu_{jk}$：类别k在观测变量j上的条件均值（剖面中心）
- $\sigma_{jk}^2$：类别k在观测变量j上的条件方差
- $Y_i$：个体i的观测变量向量

### 1.2 与LCA的根本区别

| 特征 | LPA | LCA |
|------|-----|-----|
| 观测变量 | 连续变量 | 类别/有序变量 |
| 条件分布 | 正态分布 | 条件概率分布 |
| 输出参数 | 均值、方差 | 条件概率 |
| 适用数据 | 量表得分、行为频率 | 选择型、频率型 |
| 软件实现 | Mplus、Tetrad、R | Mplus、poLCA |

### 1.3 经典文献脉络

| 作者 | 年份 | 贡献 |
|------|------|------|
| Gibson | 1959 | 潜在剖面分析原型 |
| Goodman | 1974 | 概率性潜在类别模型 |
| McLachlan & Peel | 2000 | 有限混合模型理论 |
| Vermunt & Magidson | 2002 | Latent GOLD软件实现 |
| Pastor et al. | 2007 | LPA在教育研究中的应用 |

---

## 二、模型选择与识别

### 2.1 核心指标体系

| 指标 | 判别标准 | 优先级 | 说明 |
|------|----------|--------|------|
| **BIC** | 越小越好 | ⭐⭐⭐⭐⭐ | 首选指标 |
| **aBIC** | 越小越好 | ⭐⭐⭐⭐ | 小样本首选 |
| **Entropy** | ≥ 0.80优秀 | ⭐⭐⭐⭐ | 分类精度 |
| **LMR-LRT** | p < 0.05 | ⭐⭐⭐⭐ | K vs K-1比较 |
| **BLRT** | p < 0.05 | ⭐⭐⭐⭐ | Bootstrap检验 |
| **最小剖面比例** | > 1-5% | ⭐⭐⭐⭐ | 实际意义 |

### 2.2 LPA专属考虑

**方差假设类型**：
```
variance = "const"（默认）：各类别方差相等
variance = "unequal"：各类别方差自由估计
variance = "zero"：类内无变异（理想模型）
```

**协方差假设**：
- 独立假设（默认）：类内观测变量独立
- 协方差矩阵：允许类内相关

### 2.3 模型比较决策框架

```
Step 1: 计算2-K+1个模型的BIC
Step 2: 选择BIC最小的K值
Step 3: 验证Entropy ≥ 0.80
Step 4: 检验LMR-LRT/BLRT显著性
Step 5: 检查类别比例是否合理
Step 6: 结合理论可解释性判断
```

**BIC差异解释**：
| ΔBIC | 证据强度 |
|------|----------|
| 0-2 | 微弱 |
| 2-6 | 正面 |
| 6-10 | 强烈 |
| >10 | 非常强烈 |

---

## 三、软件实现

### 3.1 Mplus语法（推荐）

```mplus
TITLE: Latent Profile Analysis;
DATA: FILE = data.csv;
       VARIABLE: NAMES = x1-x5;
                MISSING = ALL (-999);
VARIABLE: CLASSES = c(3);  ! 3个剖面
ANALYSIS: TYPE = MIXTURE;
          ESTIMATOR = MLR;  ! Robust ML
          STARTS = 200 50;
          PROCESSORS = 4;
MODEL: %OVERALL%
         %c#1%
           [x1-x5];  ! 均值
           x1-x5;    ! 方差
         %c#2%
           [x1-x5];
           x1-x5;
         %c#3%
           [x1-x5];
           x1-x5;
OUTPUT: TECH1 TECH8 TECH14;
SAVEDATA: FILE = lpa_probs.csv;
          SAVE = CPROB;
```

### 3.2 R实现（tidyLPA）

```r
library(tidyLPA)
library(dplyr)

# 数据预处理
data_clean <- data %>%
  select(x1:x5) %>%
  na.omit()

# 批量比较不同剖面数
results <- data_clean %>%
  estimate_profiles(
    n_profiles = 2:5,
    models = 1  ! model 1: 等方差，等协方差
  )

# 模型比较
compare_solutions(results)

# 最优模型详细结果
best_model <- get_fit(results)[[optimal_k]]
summary(best_model)

# 绘制剖面图
plot_profiles(results, to_center = TRUE)
```

**tidyLPA模型类型**：
| 模型 | 方差 | 协方差 | 适用场景 |
|------|------|--------|----------|
| 1 | 相等 | 0 | 默认首选 |
| 2 | 相等 | 相等 | 变量相关 |
| 3 | 不等 | 0 | 异方差 |
| 4 | 不等 | 不等 | 最复杂 |

### 3.3 R实现（MCLUST）

```r
library(mclust)

data_matrix <- as.matrix(data[, c("x1", "x2", "x3")])
fit <- Mclust(data_matrix, G = 2:4)  # G=类别数范围
summary(fit)
plot(fit, what = "BIC")
```

---

## 四、结果解释与可视化

### 4.1 剖面图（Profile Plot）

**标准化解读**：
```
z分数解读
├── z > 1.0：显著高于平均
├── 0 < z < 1：略高于平均
├── z ≈ 0：平均水平
├── -1 < z < 0：略低于平均
└── z < -1.0：显著低于平均
```

### 4.2 命名策略

- **高-中-低模式法**："高XX-中YY-低ZZ型"
- **理论构念法**：基于理论命名
- **典型特征法**：突出最显著特征

---

## 五、外生变量关联分析

### 5.1 步骤

```
Step 1: 确定最优剖面数（Step 1 LPA）
Step 2: 将类别归属作为因变量（Step 2）
Step 3: 纳入外生变量预测剖面归属
Step 4: 检验预测变量的显著性
```

### 5.2 R3STEP方法（Mplus）

```mplus
ANALYSIS: TYPE = MIXTURE;
          ESTIMATOR = MLR;

MODEL: %OVERALL%
  ! 外生变量预测类别
  c ON x1 x2 x3;

  ! 类别对结果变量的预测
  y ON c;
```

---

## 六、方法论注意事项

### 6.1 样本量要求

- **最低要求**：每个类别至少20-50个案例
- **稳定估计**：建议每类别50-100个
- **BIC最优**：通常需要200-500样本

### 6.2 稳健性检验

```
1. 改变起始值数量（STARTS = 500 100）
2. 使用不同估计器（MLR vs ML）
3. 设定不同的方差假设
4. 随机抽样验证
```

---

*LPA与LCA的选择核心：观测变量类型（连续 vs 类别/有序）*
