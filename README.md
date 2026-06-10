# Robot Data Eval Toolkit

这是一个面向 **具身智能算法实习生（数据闭环与评测方向）** 的长期学习型项目。

当前版本是 v0.1，重点展示我目前已经掌握的 Python 和 NumPy 基础能力，包括：

- Python 变量、list、dict
- for 循环和 if 判断
- 函数封装
- NumPy 数组统计
- pathlib 文件夹遍历
- 文件类型统计
- 将分析结果写入 txt 文件

## 1. 项目背景

在机器人训练和评测过程中，通常会产生大量 episode 数据，例如：

- episode_id：任务编号
- reward：任务奖励
- success：任务是否成功
- episode_length：任务执行步数
- csv / json / jpg / txt 等数据文件

本项目从一个简单版本开始，模拟机器人 episode 数据统计和数据文件夹扫描流程，为后续学习数据闭环、评测系统、数据质量分析和自动化工具开发打基础。

## 2. 当前版本：v0.1

当前版本实现了：

1. 构造机器人 episode 数据；
2. 统计总 episode 数量；
3. 统计成功 episode 数量；
4. 计算任务成功率；
5. 使用 NumPy 计算 reward 的平均值、最大值、最小值和总和；
6. 遍历 data 文件夹；
7. 统计 `.csv`、`.json`、`.jpg`、`.txt`、`.py` 文件数量；
8. 将统计结果保存到 `results/result.txt`。

## 3. 项目结构

```text
robot-data-eval-toolkit/
├── data/
│   ├── episode_log.csv
│   ├── metadata.json
│   ├── readme.txt
│   ├── sample_script.py
│   └── sample_camera.jpg
├── scripts/
│   └── analyze_robot_data.py
├── results/
│   └── result.txt
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

运行主程序：

```bash
python scripts/analyze_robot_data.py
```

运行后查看：

```text
results/result.txt
```

## 5. 示例输出

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

## 6. 与目标岗位的对应关系

| 岗位要求 | 当前项目体现 |
|---|---|
| 熟悉 Python | 使用 Python 完成数据统计脚本 |
| 熟悉 NumPy | 使用 NumPy 计算 reward 指标 |
| 数据处理 | 统计 episode 成功率和 reward |
| 数据管理 | 遍历 data 文件夹并统计文件类型 |
| 评测指标设计 | 计算 success rate、mean reward、max reward、min reward |
| 结果输出 | 自动生成 result.txt 报告 |

## 7. 后续计划

这个项目会持续迭代，不是一次性完成。

### v0.2 CSV 数据读取

- 从 `episode_log.csv` 中读取真实 episode 数据；
- 自动计算 success rate 和 reward 指标。

### v0.3 数据质量检测

- 检查缺失文件；
- 检查异常 reward；
- 检查 success 标签是否合法；
- 检查 episode_id 是否连续。

### v0.4 数据可视化

- 绘制 reward 曲线；
- 绘制 success rate 图；
- 绘制 episode_length 分布图。

### v0.5 自动化评测报告

- 自动生成更完整的 txt/json 格式报告；
- 整理成机器人数据评测小工具。

## 8. 项目说明

当前版本仍然是基础版本，但项目结构会按照长期项目维护。后续会围绕机器人数据闭环、数据评测、数据质量分析和可视化持续扩展。
