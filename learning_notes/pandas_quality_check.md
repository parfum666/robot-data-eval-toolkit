# Pandas Quality Check Notes

## v0.4 数据质量检测

在 v0.4 中，我学习了如何使用 Pandas 对机器人 episode 数据进行数据质量检测。

输入文件是：

```text
data/episodes.csv
```

每一行代表一次机器人任务执行记录，也就是一个 episode。

主要字段包括：

```text
episode_id
task
reward
success
steps
```

v0.4 的目标不是直接计算评测指标，而是在计算指标之前，先检查数据本身是否可靠。

---

## 1. 检查必要字段是否存在

机器人 episode 数据至少应该包含以下字段：

```python
REQUIRED_COLUMNS = [
    "episode_id",
    "task",
    "reward",
    "success",
    "steps",
]
```

核心代码：

```python
missing_columns = []

for col in REQUIRED_COLUMNS:
    # 如果某个必需字段不在 df.columns 中，说明 CSV 缺少这个字段
    if col not in df.columns:
        # 把缺失的字段名记录到 missing_columns 里面
        missing_columns.append(col)
```

这段代码的作用是：

```text
逐个检查 episode_id、task、reward、success、steps 是否存在。
如果某个字段缺失，就记录下来。
```

如果关键字段缺失，后面的 reward、success、steps 统计就不能继续安全进行。

---

## 2. 检查缺失值

核心代码：

```python
missing_value_summary = df.isna().sum()
```

含义：

```text
df.isna()：检查整张表每个位置是否为空
sum()：统计每一列有多少个缺失值
```

例如输出：

```text
episode_id    0
task          0
reward        1
success       0
steps         1
```

说明：

```text
reward 缺失 1 个
steps 缺失 1 个
```

继续筛选具体哪些 episode 有缺失值：

```python
episodes_with_missing_values = df[df.isna().any(axis=1)]
```

中文解释：

```text
df.isna()：得到一张 True / False 表
any(axis=1)：按行检查，只要这一行有任意一个缺失值，就返回 True
df[...]：根据 True / False 筛选出有缺失值的行
```

这句代码的作用是：

```text
找出所有存在缺失值的 episode。
```

---

## 3. 检查 success 标签是否合法

在机器人任务评测中，`success` 通常只允许两个值：

```text
1 = 成功
0 = 失败
```

如果出现：

```text
2
-1
yes
no
```

就说明 success 标签异常。

核心代码：

```python
success_numeric = pd.to_numeric(df["success"], errors="coerce")
```

中文解释：

```text
把 success 列尽量转换成数字。
如果某个值不能转换成数字，例如 yes、no，就变成 NaN。
```

继续筛选异常 success：

```python
invalid_success_episodes = df[
    # success 原始值不是空的
    df["success"].notna()
    # 并且 success 转成数字后，不属于 0 或 1
    & (~success_numeric.isin([0, 1]))
]
```

这段代码的作用是：

```text
筛选出 success 非空，但是不等于 0 或 1 的 episode。
```

注意：

```text
~ 表示取反
isin([0, 1]) 表示是否属于 0 或 1
~isin([0, 1]) 表示不属于 0 或 1
```

---

## 4. 检查 reward 是否异常

在当前项目中，暂时规定 reward 的合理范围是：

```python
REWARD_MIN = 0
REWARD_MAX = 100
```

核心代码：

```python
reward_numeric = pd.to_numeric(df["reward"], errors="coerce")
```

中文解释：

```text
把 reward 列尽量转换成数字。
如果 reward 是 bad、abc 这种内容，就会被转换成 NaN。
```

筛选异常 reward：

```python
invalid_reward_episodes = df[
    # 原始 reward 不是空值
    df["reward"].notna()
    & (
        # 原始 reward 非空，但是转换成数字失败，变成 NaN
        reward_numeric.isna()
        # reward 小于最小允许值
        | (reward_numeric < REWARD_MIN)
        # reward 大于最大允许值
        | (reward_numeric > REWARD_MAX)
    )
]
```

这段代码会筛出三类异常：

```text
1. reward 非空，但是不是数字，例如 bad、abc
2. reward 小于 REWARD_MIN，例如 -999
3. reward 大于 REWARD_MAX，例如 9999
```

这里要注意：

```text
NaN 不是 0，而是 Pandas 中表示缺失值或无效数值的标记。
```

---

## 5. 检查 steps 是否异常

`steps` 表示机器人执行一个 episode 用了多少步。

所以 steps 应该满足：

```text
能转换成数字
不能太小
不能太大
应该是整数
```

当前项目暂时设置：

```python
STEPS_MIN = 1
STEPS_MAX = 1000
```

核心代码：

```python
steps_numeric = pd.to_numeric(df["steps"], errors="coerce")
```

中文解释：

```text
把 steps 列尽量转换成数字。
如果 steps 是 bad、abc，就会变成 NaN。
```

检查 steps 是否不是整数：

```python
steps_is_not_integer = steps_numeric.notna() & (steps_numeric % 1 != 0)
```

中文解释：

```text
steps_numeric.notna()：只检查成功转换成数字的值
steps_numeric % 1 != 0：判断这个数是否有小数部分
```

例如：

```text
42 % 1 = 0，所以 42 是整数
42.5 % 1 = 0.5，所以 42.5 不是整数
```

筛选异常 steps：

```python
invalid_steps_episodes = df[
    # 原始 steps 不是空值
    df["steps"].notna()
    & (
        # steps 非空，但是转换成数字失败
        steps_numeric.isna()
        # steps 小于最小允许值
        | (steps_numeric < STEPS_MIN)
        # steps 大于最大允许值
        | (steps_numeric > STEPS_MAX)
        # steps 不是整数
        | steps_is_not_integer
    )
]
```

这段代码会筛出：

```text
bad
abc
0
-5
99999
42.5
```

这些异常 steps。

---

## 6. 检查 episode_id 是否重复

每个 episode 通常应该有唯一的 `episode_id`。

核心代码：

```python
duplicated_episode_id_episodes = df[
    # duplicated(keep=False) 会把所有重复的 episode_id 都标记出来
    df["episode_id"].duplicated(keep=False)
]
```

中文解释：

```text
duplicated()：检查某一列是否有重复值
keep=False：只要某个 episode_id 重复出现，就把所有相关行都筛出来
```

例如：

```text
episode_id
1
2
3
3
5
```

重复的是两个 `3`，使用 `keep=False` 后，两个 `3` 都会被筛出来。

这个检查可以发现：

```text
数据重复记录
合并数据时编号冲突
episode_id 生成错误
```

---

## 7. 检查 episode_id 是否连续

正常情况下，episode_id 通常应该是连续的：

```text
1, 2, 3, 4, 5
```

如果实际是：

```text
1, 2, 3, 5
```

说明：

```text
episode_id = 4 缺失
```

核心代码：

```python
episode_id_numeric = pd.to_numeric(df["episode_id"], errors="coerce")
```

中文解释：

```text
把 episode_id 尽量转换成数字。
如果 episode_id 是 abc，就会变成 NaN。
```

筛选合法的整数 episode_id：

```python
valid_episode_ids = episode_id_numeric[
    # episode_id 不是 NaN
    episode_id_numeric.notna()
    # episode_id 是整数
    & (episode_id_numeric % 1 == 0)
].astype(int)
```

中文解释：

```text
先保留非空数字，再保留整数，最后转换成 int 类型。
```

去重并排序：

```python
unique_episode_ids = sorted(valid_episode_ids.unique())
```

中文解释：

```text
unique()：去掉重复 id
sorted()：从小到大排序
```

生成理论上应该存在的 id：

```python
expected_episode_ids = set(range(1, max(unique_episode_ids) + 1))
```

中文解释：

```text
如果最大 episode_id 是 5，那么理论上应该有 1, 2, 3, 4, 5。
```

得到实际存在的 id：

```python
actual_episode_ids = set(unique_episode_ids)
```

找出缺失的 id：

```python
missing_episode_ids = sorted(expected_episode_ids - actual_episode_ids)
```

中文解释：

```text
理论上应该有的 id - 实际存在的 id = 缺失的 id
```

---

## 8. 检查 task 数据量是否均衡

机器人评测中，不同任务的数据量不能差距过大。

核心代码：

```python
task_counts = df["task"].value_counts()
```

中文解释：

```text
统计每个 task 出现了多少次。
也就是统计每个任务有多少条 episode。
```

例如：

```text
pick_cube      100
open_drawer      5
push_button      3
```

说明：

```text
pick_cube 数据很多，但 open_drawer 和 push_button 数据很少。
整体评测结果可能被 pick_cube 主导。
```

筛选样本数量过少的 task：

```python
rare_tasks = task_counts[task_counts < TASK_MIN_COUNT]
```

中文解释：

```text
找出 episode 数量少于 TASK_MIN_COUNT 的任务。
这些任务的数据量太少，评测结果可能不稳定。
```

计算 task 不均衡比例：

```python
task_imbalance_ratio = max_task_count / min_task_count
```

中文解释：

```text
最多任务的数据量 / 最少任务的数据量
```

如果这个比例太大，说明任务分布不均衡。

---

## 9. 生成数据质量检测报告

v0.4 最终会生成报告：

```text
results/data_quality_report_v04.txt
```

核心代码：

```python
report_text = "\n".join(report_lines)
```

中文解释：

```text
把 report_lines 这个列表中的每一行，用换行符连接起来，变成完整报告文本。
```

保存报告：

```python
RESULTS_DIR.mkdir(exist_ok=True)
REPORT_PATH.write_text(report_text, encoding="utf-8")
```

中文解释：

```text
RESULTS_DIR.mkdir(exist_ok=True)：确保 results 文件夹存在
REPORT_PATH.write_text(...)：把报告内容写入 txt 文件
encoding="utf-8"：避免中文乱码
```

---

## 10. v0.4 总结

v0.4 学习的重点是：

```text
在计算机器人评测指标之前，先检查数据质量。
```

本阶段完成了：

```text
1. 必需字段检查
2. 缺失值检查
3. success 标签合法性检查
4. reward 异常检查
5. steps 异常检查
6. episode_id 重复检查
7. episode_id 连续性检查
8. task 数据量均衡检查
9. 自动生成数据质量检测报告
```

相比 v0.3：

```text
v0.3 关注如何计算指标
v0.4 关注数据本身是否可靠
```

这对应机器人数据闭环与评测岗位中的一个重要能力：

```text
不能只会算成功率，还要能发现数据里的脏数据、异常值和分布问题。
```
