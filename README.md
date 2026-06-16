# Robot Data Eval Toolkit

这是一个面向 **Seed 机器人数据开发实习生 / 机器人数据平台 / 数据闭环与评测方向** 的长期学习型项目。

当前版本是 **v0.6 SQLite + FastAPI Backend**。

项目从 Python、NumPy、CSV 文件读取和 Pandas 数据分析基础出发，逐步扩展到机器人 episode 评测指标计算、失败 episode 筛选、数据质量检测、数据可视化、SQLite 数据库存储、SQL 查询以及 FastAPI 后端接口封装。

本项目的目标不是一次性完成复杂系统，而是通过持续迭代，逐步构建一个能够展示机器人数据处理、数据评测、数据质量分析、数据库查询和基础后端接口能力的 GitHub 项目。

---

## 1. 项目背景

在机器人训练、仿真和评测过程中，通常会产生大量 episode 数据，例如：

* `episode_id`：episode 编号；
* `task`：任务名称；
* `reward`：任务奖励；
* `success`：任务是否成功；
* `steps` / `episode_length`：任务执行步数；
* `failure_reason`：失败原因；
* `.csv`、`.json`、`.jpg`、`.txt`、`.png` 等数据文件。

对于机器人数据开发和数据闭环方向，除了模型训练本身，还需要对采集到的数据进行管理、清洗、统计、评测、可视化、存储和查询。

本项目从简单的数据分析脚本开始，逐步升级为一个基础的机器人 episode 数据管理与评测后端工具，用于模拟机器人数据平台中的基础数据链路：

```text
CSV 数据
→ 数据质量检查
→ 指标计算
→ 可视化分析
→ SQLite 数据库存储
→ SQL 查询
→ FastAPI 后端接口
```

---

## 2. 当前版本：v0.6 SQLite + FastAPI Backend

当前版本已经完成 **v0.6 SQLite + FastAPI 后端阶段**。

在 v0.6 中，项目新增了数据库和后端接口能力，包括：

* 使用 SQLite 创建 `episodes` 数据表；
* 将机器人 episode CSV 数据导入 SQLite 数据库；
* 使用 SQL 查询 episode 数据；
* 使用 SQL 计算整体指标：

  * `episode_count`
  * `success_rate`
  * `average_reward`
  * `average_steps`
* 使用 SQL 按 `task` 分组统计；
* 使用 SQL 查询失败 episode，也就是 badcase；
* 使用 FastAPI 封装后端接口；
* 提供 `/episodes`、`/metrics`、`/tasks`、`/badcases` API；
* 支持通过浏览器和 FastAPI 自动文档查看数据结果。

v0.6 的核心后端文件为：

```text
app/main.py
```

v0.6 的核心数据文件为：

```text
data/episodes_sql_demo.csv
```

v0.6 的 SQLite 学习脚本包括：

```text
scripts/06_create_sqlite_db.py
scripts/07_insert_one_episode.py
scripts/08_select_all_episodes.py
scripts/09_select_failed_episodes.py
scripts/10_select_episodes_by_task.py
scripts/11_sql_metrics.py
scripts/12_group_by_task_metrics.py
scripts/13_import_csv_to_sqlite.py
scripts/14_query_badcases.py
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

1. 从 `data/episodes.csv` 中读取 episode 表格数据；
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

1. 绘制 task episode 数量柱状图；
2. 绘制 reward 分布直方图；
3. 绘制 task success rate 柱状图；
4. 绘制 task average reward 柱状图；
5. 将所有图片自动保存到 `results/figures/` 文件夹；
6. 使用函数组织可视化代码。

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

### v0.6 SQLite + FastAPI Backend

v0.6 在 v0.5 的基础上，进一步从“本地数据分析脚本”升级到“基础数据管理与后端查询服务”。

v0.5 主要回答：

```text
如何对机器人 episode 数据进行可视化分析？
```

v0.6 进一步回答：

```text
如何把机器人 episode 数据存入数据库，并通过后端接口提供查询能力？
```

已实现内容包括：

1. 创建 SQLite 数据库文件：

```text
data/robot_episodes.db
```

2. 创建 `episodes` 数据表，字段包括：

```text
episode_id
task
reward
success
steps
failure_reason
```

3. 使用 SQL 创建表：

```sql
CREATE TABLE IF NOT EXISTS episodes (
    episode_id INTEGER PRIMARY KEY,
    task TEXT,
    reward REAL,
    success INTEGER,
    steps INTEGER,
    failure_reason TEXT
)
```

4. 从 `data/episodes_sql_demo.csv` 读取机器人 episode 数据；

5. 将 CSV 数据批量导入 SQLite；

6. 使用 SQL 查询全部 episode；

7. 使用 SQL 按 `task` 查询 episode；

8. 使用 SQL 查询失败 episode；

9. 使用 SQL 计算整体指标：

   * `episode_count`
   * `success_rate`
   * `average_reward`
   * `average_steps`

10. 使用 SQL 按 `task` 分组统计指标；

11. 使用 FastAPI 创建后端应用；

12. 提供以下 API 接口：

* `GET /episodes`
* `GET /episodes?task=pick_cube`
* `GET /metrics`
* `GET /tasks`
* `GET /badcases`

---

## 4. 项目结构

```text
robot-data-eval-toolkit/
├── app/
│   └── main.py
│
├── data/
│   ├── episode_log.csv
│   ├── episodes.csv
│   ├── episodes_sql_demo.csv
│   ├── metadata.json
│   ├── readme.txt
│   ├── sample_script.py
│   └── sample_camera.jpg
│
├── scripts/
│   ├── analyze_robot_data.py
│   ├── read_csv_basic.py
│   ├── pandas_read_csv_basic.py
│   ├── pandas_basic_stats.py
│   ├── pandas_groupby_task.py
│   ├── pandas_failed_episodes.py
│   ├── pandas_eval_report.py
│   ├── pandas_quality_check.py
│   ├── pandas_visualization.py
│   ├── 06_create_sqlite_db.py
│   ├── 07_insert_one_episode.py
│   ├── 08_select_all_episodes.py
│   ├── 09_select_failed_episodes.py
│   ├── 10_select_episodes_by_task.py
│   ├── 11_sql_metrics.py
│   ├── 12_group_by_task_metrics.py
│   ├── 13_import_csv_to_sqlite.py
│   └── 14_query_badcases.py
│
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
│
├── learning_notes/
│   ├── csv_basic.md
│   ├── numpy_basic.py
│   ├── pandas_basic.md
│   ├── pandas_quality_check.md
│   └── pandas_visualization.md
│
├── docs/
│   └── roadmap.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

说明：

* `data/episodes.csv` 是早期 CSV 学习阶段使用的数据；
* `data/episodes_sql_demo.csv` 是 SQLite 和 FastAPI 阶段使用的示例数据；
* `data/robot_episodes.db` 是运行脚本后生成的 SQLite 数据库文件，建议通过 `.gitignore` 忽略，不上传 GitHub；
* `scripts/` 保存各阶段学习脚本；
* `app/main.py` 是 FastAPI 后端入口文件；
* `results/` 保存报告和可视化结果；
* `learning_notes/` 保存学习笔记；
* `docs/` 保存路线规划文档。

---

## 5. 如何运行

### 5.1 安装依赖

推荐使用当前项目对应的 Python 环境运行。当前本地使用方式为：

```bash
py -3.13 -m pip install -r requirements.txt
```

`requirements.txt` 当前至少包含：

```text
numpy
pandas
matplotlib
fastapi
uvicorn
```

说明：

* `sqlite3` 是 Python 标准库，不需要写入 `requirements.txt`；
* `csv`、`pathlib` 也是 Python 标准库，不需要额外安装。

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

### 5.7 运行 v0.6 SQLite + FastAPI 后端

#### 第一步：创建 SQLite 数据库表

```bash
py -3.13 scripts/06_create_sqlite_db.py
```

该脚本会创建 SQLite 数据库文件：

```text
data/robot_episodes.db
```

并创建 `episodes` 表。

---

#### 第二步：将 CSV 数据导入 SQLite

```bash
py -3.13 scripts/13_import_csv_to_sqlite.py
```

该脚本会读取：

```text
data/episodes_sql_demo.csv
```

并将数据写入 SQLite 数据库中的 `episodes` 表。

---

#### 第三步：启动 FastAPI 后端服务

```bash
py -3.13 -m uvicorn app.main:app --reload
```

启动成功后，终端会显示：

```text
Uvicorn running on http://127.0.0.1:8000
```

然后可以访问：

```text
http://127.0.0.1:8000/docs
```

---

## 6. 示例输入

### 6.1 v0.2-v0.5 使用的 CSV 示例

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

### 6.2 v0.6 使用的 CSV 示例

`data/episodes_sql_demo.csv` 示例：

```csv
episode_id,task,reward,success,steps,failure_reason
1,pick_cube,8.5,1,42,
2,pick_cube,3.2,0,60,grasp_failed
3,pick_cube,7.8,1,45,
4,pick_cube,2.5,0,70,object_slipped
5,open_drawer,7.1,1,55,
6,open_drawer,2.4,0,80,timeout
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

All v0.5 figures have been generated successfully.
```

---

### v0.6 API 示例输出

启动 FastAPI 后端后，可以访问：

```text
http://127.0.0.1:8000/docs
```

当前提供以下 API：

| 接口                             | 功能                   |
| ------------------------------ | -------------------- |
| `GET /episodes`                | 查询所有机器人 episode 数据   |
| `GET /episodes?task=pick_cube` | 按 task 查询 episode 数据 |
| `GET /metrics`                 | 查询整体指标               |
| `GET /tasks`                   | 按 task 分组统计指标        |
| `GET /badcases`                | 查询失败 episode 数据      |

#### GET /episodes

访问：

```text
http://127.0.0.1:8000/episodes
```

返回示例：

```json
{
  "query_task": null,
  "episode_count": 20,
  "data": [
    {
      "episode_id": 1,
      "task": "pick_cube",
      "reward": 8.5,
      "success": 1,
      "steps": 42,
      "failure_reason": ""
    }
  ]
}
```

#### GET /episodes?task=pick_cube

访问：

```text
http://127.0.0.1:8000/episodes?task=pick_cube
```

返回 `task` 为 `pick_cube` 的 episode 数据。

#### GET /metrics

访问：

```text
http://127.0.0.1:8000/metrics
```

返回示例：

```json
{
  "episode_count": 20,
  "success_rate": 0.5,
  "average_reward": 5.43,
  "average_steps": 66.65
}
```

#### GET /tasks

访问：

```text
http://127.0.0.1:8000/tasks
```

返回示例：

```json
{
  "task_count": 5,
  "data": [
    {
      "task": "pick_cube",
      "episode_count": 4,
      "success_rate": 0.5,
      "average_reward": 5.5,
      "average_steps": 54.25
    }
  ]
}
```

#### GET /badcases

当前 badcase 标准：

```text
success = 0
```

访问：

```text
http://127.0.0.1:8000/badcases
```

返回示例：

```json
{
  "badcase_count": 10,
  "data": [
    {
      "episode_id": 19,
      "task": "place_cube",
      "reward": 2.7,
      "success": 0,
      "steps": 95,
      "failure_reason": "place_failed"
    }
  ]
}
```

---

## 8. 与目标岗位的对应关系

| 岗位要求          | 当前项目体现                                                        |
| ------------- | ------------------------------------------------------------- |
| Python 基础     | 使用 Python 编写 episode 数据分析、质量检测、可视化和后端接口脚本                     |
| NumPy 基础      | 使用 NumPy 计算 reward 基础统计指标                                     |
| Pandas 基础     | 使用 Pandas 读取 CSV、统计指标、筛选异常数据、分组分析                             |
| Matplotlib 基础 | 使用 Matplotlib 绘制柱状图和直方图                                       |
| SQL / SQLite  | 使用 SQLite 建表、插入数据、查询数据、聚合统计和分组统计                              |
| 数据存储          | 将机器人 episode CSV 数据导入 SQLite 数据库                              |
| 数据查询          | 支持按 task 查询 episode、查询 badcase、查询整体指标                         |
| 数据评测          | 计算 success rate、average reward、average steps                  |
| 失败案例分析        | 筛选 `success = 0` 的失败 episode，并记录 failure_reason               |
| 数据质量检测        | 检查缺失值、异常 reward、异常 steps、非法 success 标签                        |
| 数据一致性检查       | 检查 episode_id 是否重复、是否连续                                       |
| 可视化分析         | 绘制 task 数量、reward 分布、success rate、average reward 图            |
| FastAPI 后端    | 使用 FastAPI 提供 `/episodes`、`/metrics`、`/tasks`、`/badcases` 接口  |
| 数据平台理解        | 模拟从 CSV 到数据库再到 API 查询的基础数据链路                                  |
| 工程意识          | 区分 data、scripts、results、figures、learning_notes、docs、app 等项目目录 |

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
34. 自动保存可视化结果到 `results/figures/`；
35. SQLite 数据库基础；
36. `CREATE TABLE` 创建 episodes 表；
37. `INSERT INTO` 插入 episode 数据；
38. `SELECT` 查询 episode 数据；
39. `WHERE` 条件筛选；
40. `COUNT`、`AVG` 聚合统计；
41. `GROUP BY task` 分组统计；
42. CSV 批量导入 SQLite；
43. FastAPI 后端应用基础；
44. `GET /episodes` 接口；
45. `GET /metrics` 接口；
46. `GET /tasks` 接口；
47. `GET /badcases` 接口；
48. 通过 `/docs` 查看 FastAPI 自动接口文档。

当前项目已经从单纯的 Python 数据分析练习，升级为一个面向机器人 episode 数据的基础评测、数据质量检测、可视化分析和后端查询工具。

---

## 10. 可用于简历的项目描述

机器人 Episode 数据管理与评测后端工具
基于 Python、Pandas、SQLite 和 FastAPI 构建机器人 episode 数据管理与评测后端原型，实现 CSV 数据读取、数据质量检测、SQLite 存储、SQL 指标查询、任务分组统计、badcase 检索和 FastAPI 接口封装；提供 `/episodes`、`/metrics`、`/tasks`、`/badcases` 等 API，用于模拟机器人数据平台中的基础数据处理链路。

---

## 11. 后续计划

这个项目会持续迭代，但后续会以实习岗位要求为边界，不做过度复杂的后端系统。

### v0.7 MySQL / MongoDB / Parquet / ROS bag / MCAP 基础了解

后续计划补充不同数据存储与数据格式的基础理解：

* SQLite 与 MySQL 的区别；
* MongoDB 适合存储什么类型的数据；
* CSV、JSON、Parquet 的区别；
* ROS bag / MCAP 在机器人数据记录中的作用；
* 为什么机器人数据平台需要不同类型的数据存储。

---

### v0.8 数据平台基础概念

后续计划补充数据平台中的基础概念：

* 分区；
* 副本；
* 索引；
* 压缩；
* 一致性；
* 数据查询效率；
* 数据冷热分层的基础理解。

---

### v0.9 Go 语言最小数据处理与 HTTP Demo

后续计划补充 Go 语言基础，只要求能完成：

* 简单变量和结构体；
* 读取 JSON / CSV 数据；
* 简单 HTTP 服务；
* 理解 Go 在后端服务中的基础作用。

---

## 12. 项目说明

当前项目是一个学习型项目，但结构按照长期维护的方向组织。

项目从本地 CSV 数据分析开始，逐步扩展到 Pandas 数据分析、数据质量检测、可视化分析、SQLite 数据存储和 FastAPI 后端接口。通过持续迭代，本项目用于展示机器人数据开发实习岗位所需的基础能力：

* 数据读取；
* 数据清洗；
* 数据质量检查；
* 数据指标统计；
* 数据可视化；
* 数据库存储；
* SQL 查询；
* 后端接口封装；
* 数据闭环理解。

本项目后续将继续围绕机器人数据平台、数据处理链路和数据闭环方向进行轻量扩展。
