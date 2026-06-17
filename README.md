# Robot / Agent Episode Data Evaluation Toolkit

这是一个面向 **机器人数据开发、AI Agent 评测、具身智能任务评测与数据闭环方向** 的学习型项目。

当前版本为：

```text
v0.7 Storage Modeling Closing Version
```

本项目从 Python、NumPy、CSV 文件读取和 Pandas 数据分析基础出发，逐步扩展到机器人 episode 评测指标计算、失败 episode 筛选、数据质量检测、数据可视化、SQLite 数据库存储、SQL 查询、FastAPI 后端接口封装，以及 MySQL / MongoDB 存储建模理解。

项目的目标不是构建复杂后端系统，而是围绕机器人和 AI Agent 的任务执行数据，构建一个能够展示 **数据读取、数据清洗、指标评测、badcase 检索、数据库建模和基础接口封装能力** 的 GitHub 项目。

---

## 1. 项目定位

在机器人仿真、具身智能任务执行和 AI Agent 长时序任务评测中，系统通常会产生大量 episode / trajectory 数据，例如：

* `episode_id`：episode 编号；
* `task`：任务名称；
* `reward`：任务奖励；
* `success`：任务是否成功；
* `steps` / `episode_length`：任务执行步数；
* `failure_reason`：失败原因；
* `metadata`：机器人、仿真环境、相机、传感器等元信息；
* `files`：轨迹文件、图像文件、日志文件路径；
* `badcase`：失败 episode 或异常任务执行记录。

这些数据不仅可以用于机器人任务评测，也可以迁移到 AI Agent 任务评测场景中。

例如：

| 机器人 episode    | AI Agent 任务轨迹              |
| -------------- | -------------------------- |
| task           | agent task                 |
| steps          | reasoning / tool-use steps |
| success        | task success               |
| failure_reason | failure reason             |
| badcase        | failed agent trajectory    |
| trajectory     | execution trace            |

因此，本项目后续会从“机器人 episode 数据评测”逐步过渡到“机器人 / Agent episode 数据管理与评测”。

---

## 2. 项目数据链路

当前项目模拟的基础数据链路如下：

```text
CSV / JSON 数据
→ 数据读取
→ 数据质量检查
→ 指标计算
→ 可视化分析
→ SQLite 本地数据库存储
→ SQL 查询
→ FastAPI 后端接口
→ MySQL / MongoDB 存储建模理解
→ badcase 检索与评测数据管理
```

项目重点关注：

* episode 数据读取；
* success rate、average reward、average steps 等指标计算；
* task-level 分组统计；
* 失败 episode 自动筛选；
* 数据质量检测；
* 可视化分析；
* SQLite 本地存储；
* MySQL 表结构迁移理解；
* MongoDB 文档型元数据建模；
* FastAPI 查询接口封装；
* badcase 检索与数据闭环理解。

---

## 3. 当前版本说明

当前版本已经完成到：

```text
v0.7 Storage Modeling Closing Version
```

v0.7 是数据开发方向的阶段性收尾版本。

当前项目已经完成：

* Python / NumPy 基础数据处理；
* CSV episode 数据读取；
* Pandas 指标统计；
* 数据质量检测；
* Matplotlib 可视化；
* SQLite 数据库存储；
* SQL 查询与聚合统计；
* FastAPI 后端接口；
* MySQL 表结构与查询语句设计；
* MongoDB 文档型 episode 元数据建模；
* MySQL / MongoDB 与机器人 episode 数据平台场景的对应说明。

说明：

```text
MySQL / MongoDB 当前主要用于存储建模理解和代码模板展示，
不作为复杂数据库工程项目展开。
```

后续主线将转向：

```text
AI Agent 评测 + 具身智能任务评测
```

---

## 4. 已实现功能

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

v0.2 在 v0.1 的基础上，新增从 CSV 文件中读取机器人 episode 数据，并自动计算基础评测指标的功能。

已实现内容包括：

1. 从 `data/episodes.csv` 中读取 episode 表格数据；
2. 使用 `csv.DictReader` 将每一行 CSV 数据读取为字典；
3. 解析 `reward`、`success`、`steps` 字段；
4. 使用 `float()` 和 `int()` 完成类型转换；
5. 统计 episode 总数量；
6. 计算 total reward；
7. 计算 average reward；
8. 统计 success count；
9. 计算 success rate；
10. 计算 average steps；
11. 将评测结果保存到 `results/csv_eval_report_v02.txt`。

---

### v0.3 Pandas Data Analysis

v0.3 引入 Pandas，对机器人 episode 数据进行表格化分析。

已实现内容包括：

1. 使用 `pd.read_csv()` 读取 CSV 数据；
2. 使用 `df.head()` 查看 DataFrame；
3. 使用 `df.shape` 查看数据规模；
4. 计算整体评测指标：

   * episode count；
   * average reward；
   * success rate；
   * average steps；
5. 使用 `df.groupby("task")` 按任务类型分组统计；
6. 使用 `df[df["success"] == 0]` 筛选失败 episode；
7. 统计失败 episode 数量和失败率；
8. 生成 Pandas 版评测报告 `results/pandas_eval_report_v03.txt`。

---

### v0.4 Data Quality Check

v0.4 加入数据质量检测功能。

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

   * 使用 `df.isna().sum()` 统计缺失值；
   * 使用 `df[df.isna().any(axis=1)]` 筛选异常 episode。

3. 检查 `success` 标签：

   * 使用 `pd.to_numeric(..., errors="coerce")` 尝试转换；
   * 检查 `success` 是否只包含 `0` 和 `1`。

4. 检查 `reward` 异常：

   * 检查 reward 是否能转换为数字；
   * 检查 reward 是否超出设定范围。

5. 检查 `steps` 异常：

   * 检查 steps 是否能转换为数字；
   * 检查 steps 是否超出设定范围；
   * 检查 steps 是否为整数。

6. 检查 `episode_id`：

   * 检查重复 episode_id；
   * 检查 episode_id 是否连续。

7. 检查 `task` 数据量：

   * 统计每个 task 的 episode 数量；
   * 检查是否存在样本数量过少的 task。

8. 生成数据质量检测报告：

   * `results/data_quality_report_v04.txt`

---

### v0.5 Data Visualization

v0.5 加入数据可视化功能。

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

v0.6 从“本地数据分析脚本”升级到“基础数据管理与后端查询服务”。

v0.6 主要回答：

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

3. 从 `data/episodes_sql_demo.csv` 读取机器人 episode 数据；

4. 将 CSV 数据批量导入 SQLite；

5. 使用 SQL 查询全部 episode；

6. 使用 SQL 按 `task` 查询 episode；

7. 使用 SQL 查询失败 episode；

8. 使用 SQL 计算整体指标：

   * `episode_count`
   * `success_rate`
   * `average_reward`
   * `average_steps`

9. 使用 SQL 按 `task` 分组统计指标；

10. 使用 FastAPI 创建后端应用；

11. 提供以下 API 接口：

```text
GET /episodes
GET /episodes?task=pick_cube
GET /metrics
GET /tasks
GET /badcases
```

---

### v0.7 Storage Modeling Closing Version

v0.7 是数据开发方向的收尾阶段，主要补充 MySQL 和 MongoDB 的存储建模理解。

该版本不继续深入复杂后端系统、分布式系统或数据库性能优化，而是围绕岗位要求中的“熟悉 MySQL、MongoDB 等存储组件”进行轻量补充。

已完成内容包括：

1. SQLite 与 MySQL 对比说明；
2. MySQL 版 `episodes` 表结构设计；
3. MySQL 版 `INSERT`、`SELECT`、`WHERE`、`GROUP BY` 查询示例；
4. Python 连接 MySQL 的模板代码；
5. MongoDB 基础概念整理；
6. MongoDB document / collection / database 概念说明；
7. 使用 Python 字典模拟 MongoDB document；
8. 使用 Python list 模拟 MongoDB collection；
9. MongoDB 版 episode 元数据结构设计；
10. Python 连接 MongoDB 的模板代码；
11. 说明 MySQL 和 MongoDB 在机器人 / Agent episode 数据平台中的不同使用场景。

v0.7 新增文件包括：

```text
storage_demos/mysql_schema.sql
storage_demos/mysql_episode_queries.sql
storage_demos/mysql_import_episodes.py
storage_demos/mongodb_episode_document_demo.py
storage_demos/mongodb_collection_query_demo.py
storage_demos/mongodb_real_operation_template.py

docs/mysql_sqlite_notes.md
docs/mongodb_notes.md
```

---

## 5. 项目结构

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
├── storage_demos/
│   ├── mysql_schema.sql
│   ├── mysql_episode_queries.sql
│   ├── mysql_import_episodes.py
│   ├── mongodb_episode_document_demo.py
│   ├── mongodb_collection_query_demo.py
│   └── mongodb_real_operation_template.py
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
│   ├── roadmap.md
│   ├── mysql_sqlite_notes.md
│   └── mongodb_notes.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

说明：

* `data/episodes.csv` 是早期 CSV 学习阶段使用的数据；
* `data/episodes_sql_demo.csv` 是 SQLite 和 FastAPI 阶段使用的示例数据；
* `data/robot_episodes.db` 是运行脚本后生成的 SQLite 数据库文件，建议通过 `.gitignore` 忽略，不上传 GitHub；
* `scripts/` 保存各阶段 Python 学习脚本；
* `app/main.py` 是 FastAPI 后端入口文件；
* `storage_demos/` 保存 MySQL / MongoDB 存储建模与连接模板；
* `results/` 保存报告和可视化结果；
* `learning_notes/` 保存学习笔记；
* `docs/` 保存路线规划和数据库学习文档。

---

## 6. 如何运行

### 6.1 安装基础依赖

推荐使用当前项目对应的 Python 环境运行。

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
* `csv`、`pathlib` 也是 Python 标准库，不需要额外安装；
* `pymysql`、`pymongo` 当前作为 MySQL / MongoDB 连接模板的可选依赖，不作为主项目必须依赖。

---

### 6.2 运行 v0.1 基础统计脚本

```bash
py -3.13 scripts/analyze_robot_data.py
```

运行后查看：

```text
results/result.txt
```

---

### 6.3 运行 v0.2 CSV episode 评测脚本

```bash
py -3.13 scripts/read_csv_basic.py
```

运行后查看：

```text
results/csv_eval_report_v02.txt
```

---

### 6.4 运行 v0.3 Pandas 评测脚本

```bash
py -3.13 scripts/pandas_eval_report.py
```

运行后查看：

```text
results/pandas_eval_report_v03.txt
```

---

### 6.5 运行 v0.4 数据质量检测脚本

```bash
py -3.13 scripts/pandas_quality_check.py
```

运行后查看：

```text
results/data_quality_report_v04.txt
```

---

### 6.6 运行 v0.5 数据可视化脚本

```bash
py -3.13 scripts/pandas_visualization.py
```

运行后查看：

```text
results/figures/
```

---

### 6.7 运行 v0.6 SQLite + FastAPI 后端

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

启动成功后，访问：

```text
http://127.0.0.1:8000/docs
```

---

### 6.8 查看 v0.7 存储建模文件

MySQL / MongoDB 文件主要用于存储组件学习和建模说明，当前阶段不要求必须连接真实数据库服务。

可以查看：

```text
storage_demos/mysql_schema.sql
storage_demos/mysql_episode_queries.sql
storage_demos/mysql_import_episodes.py
storage_demos/mongodb_episode_document_demo.py
storage_demos/mongodb_collection_query_demo.py
storage_demos/mongodb_real_operation_template.py
```

其中，以下两个 Python 文件可以直接运行，用于理解 MongoDB 文档结构：

```bash
py -3.13 storage_demos/mongodb_episode_document_demo.py
py -3.13 storage_demos/mongodb_collection_query_demo.py
```

以下文件是连接真实数据库的模板代码，如果本地未安装 MySQL / MongoDB，可先不运行：

```text
storage_demos/mysql_import_episodes.py
storage_demos/mongodb_real_operation_template.py
```

---

## 7. API 示例

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

---

### GET /episodes

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

---

### GET /metrics

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

---

### GET /tasks

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

---

### GET /badcases

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

## 8. MySQL / MongoDB 建模说明

### 8.1 MySQL 建模

MySQL 适合保存结构化 episode 数据，例如：

```text
episode_id
task
reward
success
steps
failure_reason
```

MySQL 版 `episodes` 表结构示例：

```sql
CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT PRIMARY KEY,
    task VARCHAR(100),
    reward DOUBLE,
    success INT,
    steps INT,
    failure_reason VARCHAR(255)
);
```

在机器人 / Agent episode 数据平台中，MySQL 可以用于保存：

* episode 基础信息；
* task 维度统计；
* badcase 元数据；
* 评测任务记录；
* 数据版本信息。

---

### 8.2 MongoDB 建模

MongoDB 适合保存结构更灵活的 episode 元数据，例如：

```json
{
  "episode_id": 15,
  "task": "lift_cube",
  "reward": 2.9,
  "success": 0,
  "steps": 90,
  "failure_reason": "object_dropped",
  "metadata": {
    "robot": "Panda",
    "simulator": "robosuite",
    "camera": "frontview"
  },
  "files": {
    "trajectory": "data/trajectories/episode_15.mcap",
    "rgb_video": "data/videos/episode_15_frontview.mp4",
    "log": "data/logs/episode_15.json"
  }
}
```

在机器人 / Agent episode 数据平台中，MongoDB 可以用于保存：

* episode 元数据；
* 机器人配置；
* 仿真环境信息；
* 相机和传感器信息；
* 轨迹文件路径；
* 日志文件路径；
* 失败样本描述；
* 标注状态。

---

### 8.3 MySQL 与 MongoDB 的分工理解

一种常见设计思路是：

```text
MySQL:
保存规整的结构化数据，例如 episode_id、task、reward、success、steps。

MongoDB:
保存结构灵活的元数据，例如 robot、camera、simulator、file paths、logs。
```

二者可以通过 `episode_id` 关联。

---

## 9. 与目标岗位的对应关系

| 岗位能力要求         | 当前项目体现                                                       |
| -------------- | ------------------------------------------------------------ |
| Python 基础      | 使用 Python 编写 episode 数据分析、质量检测、可视化和后端接口脚本                    |
| NumPy / Pandas | 使用 NumPy / Pandas 完成指标统计、分组分析和异常筛选                           |
| 数据质量分析         | 检查缺失值、异常 reward、异常 steps、非法 success 标签和重复 episode_id         |
| SQL / SQLite   | 使用 SQLite 建表、插入数据、查询数据、聚合统计和分组统计                             |
| MySQL 理解       | 设计 MySQL 版 episodes 表结构和查询语句，理解关系型数据库迁移方式                    |
| MongoDB 理解     | 设计 episode 文档结构，理解 document / collection 和嵌套字段查询             |
| 数据查询           | 支持按 task 查询 episode、查询 badcase、查询整体指标                        |
| 数据评测           | 计算 success rate、average reward、average steps                 |
| badcase 分析     | 筛选 `success = 0` 的失败 episode，并记录 failure_reason              |
| 可视化分析          | 绘制 task 数量、reward 分布、success rate、average reward 图           |
| FastAPI 后端     | 提供 `/episodes`、`/metrics`、`/tasks`、`/badcases` 接口            |
| 数据平台理解         | 模拟从 CSV 到数据库再到 API 查询的基础数据链路                                 |
| AI Agent 评测迁移  | episode、steps、success、failure_reason、badcase 可迁移到 Agent 任务评测 |

---

## 10. 当前学习进度

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
26. 自动生成数据质量检测报告；
27. Matplotlib 基础可视化；
28. task episode 数量图；
29. reward 分布图；
30. task success rate 图；
31. task average reward 图；
32. SQLite 数据库基础；
33. `CREATE TABLE` 创建 episodes 表；
34. `INSERT INTO` 插入 episode 数据；
35. `SELECT` 查询 episode 数据；
36. `WHERE` 条件筛选；
37. `COUNT`、`AVG` 聚合统计；
38. `GROUP BY task` 分组统计；
39. CSV 批量导入 SQLite；
40. FastAPI 后端应用基础；
41. `GET /episodes` 接口；
42. `GET /metrics` 接口；
43. `GET /tasks` 接口；
44. `GET /badcases` 接口；
45. MySQL 与 SQLite 的区别；
46. MySQL 版 episodes 表结构设计；
47. MySQL 查询语句模板；
48. Python 连接 MySQL 模板；
49. MongoDB document / collection / database 基础；
50. MongoDB episode 文档结构设计；
51. Python 字典模拟 MongoDB document；
52. Python 列表模拟 MongoDB collection；
53. Python 连接 MongoDB 模板。

---

## 11. 可用于简历的项目描述

### 机器人 / Agent Episode 数据管理与评测工具

基于 Python、Pandas、SQLite 和 FastAPI 构建机器人 episode 数据管理与评测后端原型，实现 CSV 数据读取、数据质量检测、SQLite 存储、SQL 指标查询、任务分组统计、badcase 检索和 FastAPI 接口封装；补充 MySQL / MongoDB 存储建模理解，设计关系型 episodes 表结构与文档型 episode 元数据结构，用于模拟机器人 / Agent 任务评测中的基础数据处理链路。

---

## 12. 后续计划

当前项目的数据开发方向已经完成阶段性收尾，后续不继续深入复杂数据库工程、复杂后端系统或分布式系统实现。

后续主线将转向：

```text
AI Agent 评测 + 具身智能任务评测
```

计划继续补充：

1. AI Agent 基础概念；
2. Agent 任务轨迹与机器人 episode 的对应关系；
3. Agent task、steps、tool_calls、success、failure_reason、badcase 数据结构；
4. Agent Task Evaluation Demo；
5. RAG、工具调用、多 Agent 协作的基础理解；
6. 多模态与世界模型基础；
7. 将当前项目升级为面向机器人 / Agent episode 的评测工具。

---

## 13. 项目说明

当前项目是一个学习型项目，但按照长期维护的方向组织。

项目从本地 CSV 数据分析开始，逐步扩展到 Pandas 数据分析、数据质量检测、可视化分析、SQLite 数据存储、FastAPI 后端接口、MySQL / MongoDB 存储建模理解。

通过持续迭代，本项目用于展示以下能力：

* 数据读取；
* 数据清洗；
* 数据质量检查；
* 数据指标统计；
* 数据可视化；
* 数据库存储；
* SQL 查询；
* 后端接口封装；
* MySQL / MongoDB 存储建模理解；
* badcase 检索；
* 机器人 / Agent episode 评测理解；
* 数据闭环意识。

后续将围绕 AI Agent 评测、具身智能任务评测和多模态任务数据分析继续扩展。
