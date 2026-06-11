# Robot Data Eval Toolkit

这是一个面向 **具身智能算法实习生（数据闭环与评测方向）** 的长期学习型项目。

当前版本是 **v0.2**。项目从 Python 和 NumPy 基础出发，逐步扩展到 CSV episode 数据读取、机器人评测指标计算和自动化评测报告生成。

目前项目重点展示我已经掌握的能力包括：

* Python 变量、list、dict
* for 循环和 if 判断
* 函数封装
* NumPy 数组统计
* pathlib 文件夹遍历
* 文件类型统计
* CSV 文件读取
* 使用 `csv.DictReader` 解析 episode 数据
* reward、success、steps 字段类型转换
* 计算 average reward、success rate、average steps
* 将分析结果写入 txt 文件

## 1. 项目背景

在机器人训练和评测过程中，通常会产生大量 episode 数据，例如：

* episode_id：任务编号
* task：任务名称
* reward：任务奖励
* success：任务是否成功
* steps / episode_length：任务执行步数
* csv / json / jpg / txt 等数据文件

对于具身智能算法的数据闭环与评测方向，除了训练模型本身，还需要对采集到的数据进行管理、清洗、统计、评测和回流。本项目从一个简单版本开始，模拟机器人 episode 数据统计和数据文件夹扫描流程，为后续学习数据闭环、评测系统、数据质量分析和自动化工具开发打基础。

## 2. 当前版本：v0.2

当前版本在 v0.1 的基础上，新增了从 CSV 文件中读取机器人 episode 数据，并自动计算基础评测指标的功能。

### v0.1 已实现内容

1. 构造机器人 episode 数据；
2. 统计总 episode 数量；
3. 统计成功 episode 数量；
4. 计算任务成功率；
5. 使用 NumPy 计算 reward 的平均值、最大值、最小值和总和；
6. 遍历 data 文件夹；
7. 统计 `.csv`、`.json`、`.jpg`、`.txt`、`.py` 文件数量；
8. 将统计结果保存到 `results/result.txt`。

### v0.2 新增内容

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
12. 将 CSV 评测结果保存到 `results/csv_eval_report_v02.txt`，避免覆盖旧版本结果文件。

## 3. 项目结构

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
│   └── read_csv_basic.py
├── results/
│   ├── result.txt
│   └── csv_eval_report_v02.txt
├── learning_notes/
│   └── numpy_basic.py
├── docs/
│   └── roadmap.md
├── requirements.txt
├── .gitignore
└── README.md
```

## 4. 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

运行 v0.1 主程序：

```bash
python scripts/analyze_robot_data.py
```

运行后查看：

```text
results/result.txt
```

运行 v0.2 CSV episode 评测程序：

```bash
python scripts/read_csv_basic.py
```

运行后查看：

```text
results/csv_eval_report_v02.txt
```

## 5. 示例输入

`data/episodes.csv` 示例：

```csv
episode_id,task,reward,success,steps
1,pick_cube,8.5,1,42
2,pick_cube,3.2,0,60
3,open_drawer,7.1,1,55
4,open_drawer,2.4,0,80
5,push_button,9.0,1,35
```

## 6. 示例输出

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

## 7. 与目标岗位的对应关系

| 岗位要求      | 当前项目体现                                       |
| --------- | -------------------------------------------- |
| 熟悉 Python | 使用 Python 完成 episode 数据统计脚本                  |
| 熟悉 NumPy  | 使用 NumPy 计算 reward 指标                        |
| 熟悉数据处理    | 从 CSV 文件中读取并解析 episode 数据                    |
| 熟悉数据管理    | 遍历 data 文件夹并统计文件类型                           |
| 评测指标设计与实现 | 计算 average reward、success rate、average steps |
| 数据质量分析基础  | 初步检查 reward、success、steps 等核心字段              |
| 自动化评测工具开发 | 自动生成 txt 格式评测报告                              |
| 良好的工程意识   | 区分 data、scripts、results、docs 等项目目录           |
| 数据闭环理解    | 模拟从 episode 数据读取到评测报告生成的基础流程                 |

## 8. 当前学习进度

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
11. 基础评测报告生成。

当前项目已经从单纯的 Python 练习，升级为一个面向机器人 episode 数据的基础评测工具。

## 9. 后续计划

这个项目会持续迭代，不是一次性完成。

### v0.3 Pandas 数据分析

* 使用 `pandas.read_csv()` 读取 episode 数据；
* 使用 `df.head()`、`df.shape`、`df.columns` 查看数据；
* 使用 `df["reward"].mean()` 计算平均 reward；
* 使用 `df["success"].mean()` 计算 success rate；
* 使用 `groupby("task")` 按任务类型统计指标；
* 筛选失败 episode；
* 生成 Pandas 版本评测报告。

### v0.4 数据质量检测

* 检查缺失值；
* 检查异常 reward；
* 检查 success 标签是否合法；
* 检查 steps 是否异常；
* 检查 episode_id 是否连续；
* 检查不同 task 的数据量是否均衡。

### v0.5 数据可视化

* 绘制 reward 曲线；
* 绘制 success rate 图；
* 绘制 average steps 图；
* 绘制不同 task 的指标对比图；
* 保存可视化结果到 `results/figures/`。

### v0.6 自动化评测报告

* 自动生成更完整的 txt/json 格式报告；
* 汇总 reward、success、steps、异常 episode；
* 整理成机器人数据评测小工具；
* 为后续数据闭环、数据筛选和模型评测做准备。

## 10. 项目说明

当前版本仍然是基础版本，但项目结构会按照长期项目维护。后续会围绕机器人数据闭环、数据评测、数据质量分析和可视化持续扩展。

本项目的目标不是一次性完成复杂系统，而是通过持续迭代，逐步把 Python、NumPy、Pandas、数据质量检测、可视化和机器人评测指标结合起来，形成一个能够展示岗位匹配度的学习型 GitHub 项目。
