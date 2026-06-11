# CSV Basic Notes

本笔记记录 `robot-data-eval-toolkit` 项目 v0.2 阶段的学习内容。该阶段主要学习如何使用 Python 读取 CSV 格式的机器人 episode 数据，并计算基础评测指标。

## 1. CSV 文件的作用

CSV 可以理解为一种表格文件。在机器人训练和评测过程中，一行数据通常可以表示一次 episode。

本阶段使用的示例字段包括：

* `episode_id`：episode 编号
* `task`：任务名称
* `reward`：任务奖励
* `success`：任务是否成功，1 表示成功，0 表示失败
* `steps`：任务执行步数

示例数据：

```csv
episode_id,task,reward,success,steps
1,pick_cube,8.5,1,42
2,pick_cube,3.2,0,60
3,open_drawer,7.1,1,55
```

## 2. 使用 pathlib 管理文件路径

本阶段继续使用 `pathlib` 来管理文件路径：

```python
from pathlib import Path

csv_path = Path("data") / "episodes.csv"
report_path = Path("results") / "csv_eval_report_v02.txt"
```

其中：

```python
csv_path
```

是变量，表示保存路径信息的对象。

而：

```python
"csv_path"
```

是字符串，表示普通文字。

所以打开文件时应写：

```python
open(csv_path, "r", encoding="utf-8")
```

而不是：

```python
open("csv_path", "r", encoding="utf-8")
```

## 3. 使用 csv.DictReader 读取 CSV

核心代码：

```python
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
```

`csv.DictReader(f)` 的作用是根据 CSV 第一行表头，把后面的每一行数据读取成字典。

例如 CSV 中的一行：

```csv
1,pick_cube,8.5,1,42
```

会被读取成：

```python
{
    "episode_id": "1",
    "task": "pick_cube",
    "reward": "8.5",
    "success": "1",
    "steps": "42"
}
```

这样后续就可以通过字段名取值：

```python
row["task"]
row["reward"]
row["success"]
row["steps"]
```

## 4. with open 的缩进问题

读取文件的循环必须写在 `with open(...)` 的缩进里面。

正确写法：

```python
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row)
```

错误写法：

```python
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

for row in reader:
    print(row)
```

错误原因是：退出 `with open(...)` 的缩进范围后，文件已经自动关闭，再读取就会出现：

```text
ValueError: I/O operation on closed file.
```

## 5. CSV 读取后的类型转换

CSV 读出来的数据默认都是字符串。

例如：

```python
row["reward"]
```

读出来是：

```python
"8.5"
```

而不是：

```python
8.5
```

所以要使用 `float()` 转换 reward：

```python
reward = float(row["reward"])
```

对于 success 和 steps，要使用 `int()` 转换：

```python
success = int(row["success"])
steps = int(row["steps"])
```

## 6. 累计 total reward

初始化总 reward：

```python
total_reward = 0
```

每读取一条 episode，就累加一次：

```python
total_reward = total_reward + reward
```

这句代码的意思是：

把当前 episode 的 reward 加到之前已经累计的总 reward 里面。

## 7. 统计 episode 数量

初始化 episode 计数器：

```python
episode_count = 0
```

每读取一条 episode，就加 1：

```python
episode_count = episode_count + 1
```

最后可以计算平均 reward：

```python
average_reward = total_reward / episode_count
```

## 8. 统计 success rate

初始化成功数量：

```python
success_count = 0
```

判断当前 episode 是否成功：

```python
if success == 1:
    success_count = success_count + 1
```

计算成功率：

```python
success_rate = success_count / episode_count
```

在机器人评测中，success rate 是非常重要的指标。它可以反映模型真正完成任务的比例。

## 9. 统计 average steps

初始化总步数：

```python
total_steps = 0
```

每读取一条 episode，累加 steps：

```python
total_steps = total_steps + steps
```

计算平均步数：

```python
average_steps = total_steps / episode_count
```

average steps 可以反映机器人完成任务的效率。当 success rate 相同的时候，average steps 更低通常代表执行效率更高。

## 10. 写入评测报告

报告路径：

```python
report_path = Path("results") / "csv_eval_report_v02.txt"
```

写入文件：

```python
with open(report_path, "w", encoding="utf-8") as f:
    f.write("Robot Episode Evaluation Report\n")
```

其中：

```python
"w"
```

表示覆盖写入。如果文件已经存在，原内容会被清空。

因此本项目中没有继续写入 `results/result.txt`，而是新建：

```text
results/csv_eval_report_v02.txt
```

避免覆盖 v0.1 的结果。

## 11. 本阶段完成的指标

v0.2 阶段最终完成了以下指标：

* episode count
* total reward
* average reward
* success count
* success rate
* average steps

这些指标对应机器人评测中的基础评测能力，可以用于初步判断一批 episode 数据的整体表现。

## 12. 与岗位能力的对应关系

本阶段内容对应岗位中的以下能力：

* 数据全生命周期中的数据读取
* 机器人 episode 数据解析
* 基础评测指标设计与实现
* 自动化评测结果输出
* 数据管理和工程目录组织
* 为后续 Pandas、数据质量检测、可视化分析打基础
