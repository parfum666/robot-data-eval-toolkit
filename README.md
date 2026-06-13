# Robot Data Eval Toolkit

这是一个面向 **具身智能算法实习生（数据闭环与评测方向）** 的长期学习型项目。

当前版本是 **v0.5**。项目从 Python、NumPy、文件读写和 CSV 解析基础出发，逐步扩展到 Pandas 数据分析、机器人 episode 评测指标计算、失败 episode 筛选、数据质量检测、数据可视化和自动化报告生成。

本项目的目标不是一次性完成复杂系统，而是通过持续迭代，逐步构建一个能够展示机器人数据处理、评测分析、数据质量检查、可视化分析和数据闭环理解能力的 GitHub 项目。

---

## 1. 项目背景

在机器人训练和评测过程中，通常会产生大量 episode 数据，例如：

* `episode_id`：episode 编号
* `task`：任务名称
* `reward`：任务奖励
* `success`：任务是否成功
* `steps` / `episode_length`：任务执行步数
* `.csv`、`.json`、`.jpg`、`.txt`、`.png` 等数据文件

对于具身智能算法的数据闭环与评测方向，除了训练模型本身，还需要对采集到的数据进行管理、清洗、统计、评测、可视化和回流。

本项目从一个简单版本开始，模拟机器人 episode 数据统计、数据文件夹扫描、Pandas 数据分析、数据质量检测和可视化分析流程，为后续学习数据闭环、评测系统、数据质量分析和自动化工具开发打基础。

---

## 2. 当前版本：v0.5 Data Visualization

当前版本已经完成 **v0.5 数据可视化阶段**。

在 v0.5 中，项目新增了基于 Pandas 和 Matplotlib 的机器人 episode 数据可视化功能，包括：

* 绘制每个 `task` 的 episode 数量柱状图；
* 绘制所有 episode 的 reward 分布直方图；
* 绘制每个 `task` 的 success rate 柱状图；
* 绘制每个 `task` 的 average reward 柱状图；
* 将所有图片自动保存到 `results/figures/` 文件夹。

v0.5 的最终整合脚本为：

```text
scripts/pandas_visualization.py
```

v0.5 的输出图片包括：

```text
results/figures/task_episode_count_v05.png
results/figures/reward_distribution_v05.png
results/figures/task_success_rate_v05.png
results/figures/task_average_reward_v05.png
```

---

## 3. 已实现功能

### v0.1 Python + NumPy 基础评测

v0.1 主要完成 Python 和 NumPy 基础练习，并初步模拟机器人 episode 统计。

已实现内容包括：

1. 构造机器人 episode 数据；
2. 统计总 episode 数量；
3. 统计成功 episode 数量；
4. 计算任务成功率；
5. 使用 NumPy 计算 reward 的平均值、最大值、最小值和总和；
6. 使用 `pathlib` 遍历 `data/` 文件夹；
7. 统计 `.csv`、`.json`、`.jpg`、`.txt`、`.py` 文件数量；
8. 将统计结果保存到 `results/result.txt`。

---

### v0.2 CSV Episode Evaluation

v0.2 在 v0.1 的基础上，新增了从 CSV 文件中读取机器人 episode 数据，并自动计算基础评测指标的功能。

已实现内容包括：

1. 从 `data/episodes.csv` 中读取真实 episode 表格数据；
2. 使用 `csv.DictReader` 将每一行 CSV 数据读取为字典；
3. 读取并解析 `reward`、`success`、`steps` 字段；
4. 使用 `float()` 将 reward 从字符串转换为小数；
5. 使用 `int()` 将 success 和 steps 从字符串转换为整数；
6. 统计 episode 总数量；
7. 计算 total reward；
8. 计算 average reward；
9. 统计 success count；
10. 计算 success rate；
11. 计算 average steps；
12. 将 CSV 评测结果保存到 `results/csv_eval_report_v02.txt`。

---

### v0.3 Pandas Data Analysis

v0.3 在 v0.2 的基础上，引入 Pandas，对机器人 episode 数据进行更高效的表格化分析。

已实现内容包括：

1. 使用 `pd.read_csv()` 读取 CSV 数据；
2. 使用 `df.head()` 查看 DataFrame 前几行；
3. 使用 `df.shape` 查看数据规模；
4. 使用 `df.columns` 查看字段名称；
5. 使用 `df["reward"]` 取出单列数据；
6. 计算整体评测指标：

   * episode count
   * average reward
   * success rate
   * average steps
7. 使用 `df.groupby("task")` 按任务类型分组统计指标；
8. 生成 task-level evaluation report；
9. 使用 `df[df["success"] == 0]` 筛选失败 episode；
10. 统计失败 episode 数量和失败率；
11. 使用 `value_counts()` 统计失败 episode 主要集中在哪些 task；
12. 生成 Pandas 版评测报告 `results/pandas_eval_report_v03.txt`。

---

### v0.4 Data Quality Check

v0.4 在 v0.3 的基础上，进一步加入数据质量检测功能。

v0.3 主要回答：

```text
这批机器人 episode 数据的评测指标是多少？
```

v0.4 进一步回答：

```text
这批机器人 episode 数据本身是否可靠？
```

已实现内容包括：

1. 检查必要字段：

   * `episode_id`
   * `task`
   * `reward`
   * `success`
   * `steps`

2. 检查缺失值：

   * 使用 `df.isna().sum()` 统计每一列缺失值数量；
   * 使用 `df[df.isna().any(axis=1)]` 筛选存在缺失值的 episode。

3. 检查 `success` 标签：

   * 使用 `pd.to_numeric(..., errors="coerce")` 尝试转换为数字；
   * 检查 `success` 是否只包含 `0` 和 `1`；
   * 筛选非法 success 标签。

4. 检查 `reward` 异常：

   * 检查 reward 是否能转换为数字；
   * 检查 reward 是否小于 `REWARD_MIN`；
   * 检查 reward 是否大于 `REWARD_MAX`；
   * 筛选非空但异常的 reward episode。

5. 检查 `steps` 异常：

   * 检查 steps 是否能转换为数字；
   * 检查 steps 是否小于 `STEPS_MIN`；
   * 检查 steps 是否大于 `STEPS_MAX`；
   * 检查 steps 是否为整数。

6. 检查 `episode_id`：

   * 使用 `duplicated(keep=False)` 检查重复 episode_id；
   * 检查 episode_id 是否从 1 开始连续递增；
   * 输出缺失的 episode_id。

7. 检查 `task` 数据量：

   * 使用 `value_counts()` 统计每个 task 的 episode 数量；
   * 检查是否存在样本数量过少的 task；
   * 检查 task 数据分布是否不均衡。

8. 生成数据质量检测报告：

   * 输出到 `results/data_quality_report_v04.txt`。

---

### v0.5 Data Visualization

v0.5 在 v0.4 的基础上，进一步加入数据可视化功能。

v0.4 主要回答：

```text
数据有没有缺失、异常、不连续、不均衡？
```

v0.5 进一步回答：

```text
这些数据问题和评测结果能不能用图更直观地展示出来？
```

已实现内容包括：

1. 绘制 task episode 数量柱状图：

   * 使用 `df["task"].value_counts()` 统计每个 task 的 episode 数量；
   * 使用 `plt.bar()` 绘制柱状图；
   * 输出到 `results/figures/task_episode_count_v05.png`。

2. 绘制 reward 分布直方图：

   * 使用 `pd.to_numeric()` 将 reward 转换为数字；
   * 使用 `dropna()` 去除无效 reward；
   * 使用 `plt.hist()` 绘制 reward 分布；
   * 输出到 `results/figures/reward_distribution_v05.png`。

3. 绘制 task success rate 柱状图：

   * 使用 `pd.to_numeric()` 清洗 success；
   * 使用 `groupby("task")["success"].mean()` 计算每个 task 的成功率；
   * 使用 `plt.bar()` 绘制每个 task 的 success rate；
   * 输出到 `results/figures/task_success_rate_v05.png`。

4. 绘制 task average reward 柱状图：

   * 使用 `pd.to_numeric()` 清洗 reward；
   * 使用 `groupby("task")["reward"].mean()` 计算每个 task 的平均 reward；
   * 使用 `plt.bar()` 绘制每个 task 的 average reward；
   * 输出到 `results/figures/task_average_reward_v05.png`。

5. 使用函数组织可视化代码：

   * `plot_task_episode_count(df)`
   * `plot_reward_distribution(df)`
   * `plot_task_success_rate(df)`
   * `plot_task_average_reward(df)`

---

## 4. 项目结构

```text
robot-data-eval-toolkit/
├── data/
│   ├── episode_log.csv
│   ├── episodes.csv
│   ├── metadata.json
│   ├── readme.txt
│   ├── sample_script.py
│   └── sample_camera.jpg
├── scripts/
│   ├── analyze_robot_data.py
│   ├── read_csv_basic.py
│   ├── pandas_read_csv_basic.py
│   ├── pandas_basic_stats.py
│   ├── pandas_groupby_task.py
│   ├── pandas_failed_episodes.py
│   ├── pandas_eval_report.py
│   ├── pandas_quality_check.py
│   └── pandas_visualization.py
├── results/
│   ├── result.txt
│   ├── csv_eval_report_v02.txt
│   ├── pandas_eval_report_v03.txt
│   ├── data_quality_report_v04.txt
│   └── figures/
│       ├── task_episode_count_v05.png
│       ├── reward_distribution_v05.png
│       ├── task_success_rate_v05.png
│       └── task_average_reward_v05.png
├── learning_notes/
│   ├── csv_basic.md
│   ├── pandas_basic.md
│   ├── pandas_quality_check.md
│   └── pandas_visualization.md
├── docs/
│   └── roadmap.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 5. 如何运行

### 5.1 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 当前至少需要包含：

```text
numpy
pandas
matplotlib
```

如果当前电脑的 `python` 环境不是 Anaconda，也可以使用指定 Python 解释器运行，例如：

```bash
D:\anaconda\python.exe scripts\pandas_visualization.py
```

---

### 5.2 运行 v0.1 基础统计脚本

```bash
python scripts/analyze_robot_data.py
```

运行后查看：

```text
results/result.txt
```

---

### 5.3 运行 v0.2 CSV episode 评测脚本

```bash
python scripts/read_csv_basic.py
```

运行后查看：

```text
results/csv_eval_report_v02.txt
```

---

### 5.4 运行 v0.3 Pandas 评测脚本

```bash
python scripts/pandas_eval_report.py
```

运行后查看：

```text
results/pandas_eval_report_v03.txt
```

---

### 5.5 运行 v0.4 数据质量检测脚本

```bash
python scripts/pandas_quality_check.py
```

运行后查看：

```text
results/data_quality_report_v04.txt
```

---

### 5.6 运行 v0.5 数据可视化脚本

```bash
python scripts/pandas_visualization.py
```

运行后查看：

```text
results/figures/task_episode_count_v05.png
results/figures/reward_distribution_v05.png
results/figures/task_success_rate_v05.png
results/figures/task_average_reward_v05.png
```

---

## 6. 示例输入

`data/episodes.csv` 示例：

```csv
episode_id,task,reward,success,steps
1,pick_cube,8.5,1,42
2,pick_cube,3.2,0,60
3,open_drawer,7.1,1,55
4,open_drawer,2.4,0,80
5,push_button,9.0,1,35
```

---

## 7. 示例输出

### v0.1 示例输出

```text
Robot Episode Statistics
Total Episodes: 5
Success Count: 3
Success Rate: 60.00%

Reward Statistics
Mean Reward: 26.00
Max Reward: 40
Min Reward: 15
Sum Reward: 130

Data Folder Statistics
CSV Files: 1
JSON Files: 1
JPG Files: 1
TXT Files: 1
PY Files: 1
```

---

### v0.2 示例输出

```text
Robot Episode Evaluation Report
===============================
episode count: 5
total reward: 30.2
average reward: 6.04
success count: 3
success rate: 0.6
average steps: 54.4
```

---

### v0.3 示例输出

```text
Pandas Robot Episode Evaluation Report v0.3
================================================

Overall Evaluation
------------------------------------------------
Total episode count: 5
Average reward: 6.04
Success rate: 0.6
Average steps: 54.4

Task-level Evaluation Report
------------------------------------------------
             episode_count  average_reward  success_rate  average_steps
task
open_drawer              2            4.75           0.5           67.5
pick_cube                2            5.85           0.5           51.0
push_button              1            9.00           1.0           35.0
```

---

### v0.4 示例输出

```text
Robot Episode Data Quality Report v0.4
================================================

Required Column Check
------------------------------------------------
All required columns exist.

Missing Value Summary
------------------------------------------------
episode_id    0
task          0
reward        0
success       0
steps         0

Reward Check Summary
------------------------------------------------
Reward valid range: [0, 100]
Invalid reward count: 0
Invalid reward rate: 0.0

Steps Check Summary
------------------------------------------------
Steps valid range: [1, 1000]
Invalid steps count: 0
Invalid steps rate: 0.0

Task Episode Count
------------------------------------------------
pick_cube      2
open_drawer    2
push_button    1
```

---

### v0.5 示例输出

v0.5 会自动生成 4 张图片：

```text
results/figures/task_episode_count_v05.png
results/figures/reward_distribution_v05.png
results/figures/task_success_rate_v05.png
results/figures/task_average_reward_v05.png
```

终端输出示例：

```text
Task Episode Count
--------------------------------
pick_cube      2
open_drawer    2
push_button    1

Reward Summary
--------------------------------
count    5.000000
mean     6.040000
min      2.400000
max      9.000000

Task Success Rate
--------------------------------
open_drawer    0.5
pick_cube      0.5
push_button    1.0

Task Average Reward
--------------------------------
open_drawer    4.75
pick_cube      5.85
push_button    9.00

All v0.5 figures have been generated successfully.
```

---

## 8. 与目标岗位的对应关系

| 岗位要求          | 当前项目体现                                                    |
| ------------- | --------------------------------------------------------- |
| 熟悉 Python     | 使用 Python 编写 episode 数据分析、质量检测和可视化脚本                      |
| 熟悉 NumPy      | 使用 NumPy 计算 reward 的基础统计指标                                |
| 熟悉 Pandas     | 使用 Pandas 读取 CSV、统计指标、筛选异常数据、分组分析                         |
| 熟悉 Matplotlib | 使用 Matplotlib 绘制柱状图和直方图                                   |
| 熟悉数据处理        | 从 CSV 文件中读取并解析 episode 数据                                 |
| 熟悉数据管理        | 遍历 data 文件夹并统计不同类型的数据文件                                   |
| 评测指标设计与实现     | 计算 average reward、success rate、average steps              |
| 任务级评测分析       | 使用 `groupby("task")` 分析不同任务表现                             |
| 失败数据分析        | 筛选 `success == 0` 的失败 episode                             |
| 数据质量检测        | 检查缺失值、异常 reward、异常 steps、非法 success 标签                    |
| 数据一致性检查       | 检查 episode_id 是否重复、是否连续                                   |
| 数据分布分析        | 检查不同 task 的 episode 数量是否均衡                                |
| 可视化分析         | 绘制 task 数量、reward 分布、success rate、average reward 图        |
| 数据闭环理解        | 从整体指标进一步定位失败任务、脏数据和低表现任务，为后续数据回流做准备                       |
| 自动化评测工具开发     | 自动生成 txt 格式评测报告、数据质量报告和可视化图片                              |
| 良好的工程意识       | 区分 data、scripts、results、figures、learning_notes、docs 等项目目录 |

---

## 9. 当前学习进度

目前已经完成：

1. Python 基础语法；
2. list、dict、for、if、函数；
3. 文件读取和写入；
4. pathlib 文件路径管理；
5. 文件夹遍历和文件类型统计；
6. NumPy 基础统计；
7. CSV 文件读取；
8. `csv.DictReader` 的使用；
9. 字符串到数字的类型转换；
10. episode count、average reward、success rate、average steps 的计算；
11. Pandas 读取 CSV；
12. DataFrame 基础查看；
13. Pandas 单列统计；
14. Pandas 按 task 分组统计；
15. Pandas 筛选失败 episode；
16. 失败 episode 的 task 分布统计；
17. 自动生成 Pandas 版评测报告；
18. 必要字段检查；
19. 缺失值检查；
20. success 标签合法性检查；
21. reward 异常检查；
22. steps 异常检查；
23. episode_id 重复检查；
24. episode_id 连续性检查；
25. task 数据量均衡检查；
26. 自动生成 v0.4 数据质量检测报告；
27. 使用 Matplotlib 绘制柱状图；
28. 使用 Matplotlib 绘制直方图；
29. 绘制 task episode 数量图；
30. 绘制 reward 分布图；
31. 绘制 task success rate 图；
32. 绘制 task average reward 图；
33. 使用函数组织可视化代码；
34. 自动保存可视化结果到 `results/figures/`。

当前项目已经从单纯的 Python 练习，升级为一个面向机器人 episode 数据的基础评测、数据质量检测和可视化分析工具。

---

## 10. 后续计划

这个项目会持续迭代，不是一次性完成。

### v0.6 自动化评测报告增强

后续计划生成更完整的自动化评测报告，包括：

* 汇总 reward、success、steps；
* 汇总 task-level 评测指标；
* 汇总失败 episode；
* 汇总异常 episode；
* 汇总数据质量检测结果；
* 汇总可视化图片路径；
* 支持 txt / json 格式报告；
* 为后续数据闭环、数据筛选和模型评测做准备。

---

### v0.7 数据闭环模拟

后续计划进一步模拟数据闭环流程，包括：

* 根据失败 episode 筛选需要回流的数据；
* 根据异常数据生成清洗建议；
* 根据 task 分布生成补采样建议；
* 根据低 success rate 任务生成重点分析建议；
* 将质量检测结果、评测指标和可视化结果结合，形成更完整的数据闭环分析工具。

---

## 11. 项目说明

当前版本仍然是基础版本，但项目结构会按照长期项目维护。

本项目会围绕机器人数据闭环、数据评测、数据质量分析和可视化持续扩展。通过持续迭代，本项目将逐步把 Python、NumPy、Pandas、Matplotlib、数据质量检测、可视化和机器人评测指标结合起来，形成一个能够展示岗位匹配度的学习型 GitHub 项目。
