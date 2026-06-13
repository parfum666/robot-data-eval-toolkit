# Pandas Visualization Notes

## v0.5 数据可视化

在 v0.5 中，我学习了如何使用 Pandas 和 Matplotlib 对机器人 episode 数据进行可视化分析。

输入文件是：

```text
data/episodes.csv
```

输出图片保存到：

```text
results/figures/
```

v0.5 的目标是把 v0.3 和 v0.4 中计算出来的数据指标，用图片的形式展示出来。

相比纯文本报告，图片可以更直观地展示：

```text
1. 不同 task 的 episode 数量是否均衡
2. reward 整体分布情况
3. 不同 task 的 success rate
4. 不同 task 的 average reward
```

---

## 1. Matplotlib 基础

本阶段使用：

```python
import matplotlib.pyplot as plt
```

`matplotlib.pyplot` 是 Python 中常用的画图库。

在项目中，我把它简写为：

```python
plt
```

之后就可以用：

```python
plt.figure()
plt.bar()
plt.hist()
plt.title()
plt.xlabel()
plt.ylabel()
plt.savefig()
plt.close()
```

来创建和保存图像。

---

## 2. 图片保存路径

核心代码：

```python
FIGURES_DIR = Path("results") / "figures"

TASK_COUNT_FIGURE_PATH = FIGURES_DIR / "task_episode_count_v05.png"
REWARD_DISTRIBUTION_FIGURE_PATH = FIGURES_DIR / "reward_distribution_v05.png"
TASK_SUCCESS_RATE_FIGURE_PATH = FIGURES_DIR / "task_success_rate_v05.png"
TASK_AVERAGE_REWARD_FIGURE_PATH = FIGURES_DIR / "task_average_reward_v05.png"
```

中文解释：

```text
FIGURES_DIR 表示图片保存文件夹。
所有 v0.5 生成的图片都放在 results/figures/ 下面。
```

在 `main()` 里面使用：

```python
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
```

中文解释：

```text
parents=True：如果 results 文件夹不存在，也会一起创建。
exist_ok=True：如果 results/figures 已经存在，也不会报错。
```

---

## 3. 绘制 task episode 数量柱状图

对应函数：

```python
def plot_task_episode_count(df):
```

作用：

```text
统计每个 task 有多少条 episode，并画成柱状图。
```

核心代码：

```python
task_counts = df["task"].value_counts()
```

中文解释：

```text
df["task"]：取出 task 这一列
value_counts()：统计每个 task 出现了多少次
```

例如：

```text
pick_cube
pick_cube
open_drawer
open_drawer
push_button
```

统计结果是：

```text
pick_cube      2
open_drawer    2
push_button    1
```

画图代码：

```python
plt.figure(figsize=(8, 5))

plt.bar(task_counts.index, task_counts.values)

plt.title("Episode Count by Task")
plt.xlabel("Task")
plt.ylabel("Episode Count")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(TASK_COUNT_FIGURE_PATH)
plt.close()
```

中文解释：

```text
plt.figure(figsize=(8, 5))：创建一张宽 8、高 5 的图
plt.bar(...)：绘制柱状图
task_counts.index：横轴，是 task 名称
task_counts.values：纵轴，是每个 task 的 episode 数量
plt.title(...)：设置图标题
plt.xlabel(...)：设置 x 轴名称
plt.ylabel(...)：设置 y 轴名称
plt.xticks(rotation=30)：让横轴文字旋转 30 度，避免重叠
plt.tight_layout()：自动调整布局，防止文字被裁掉
plt.savefig(...)：保存图片
plt.close()：关闭当前图，避免影响下一张图
```

输出图片：

```text
results/figures/task_episode_count_v05.png
```

这张图回答的问题是：

```text
每个任务有多少数据？
```

它主要用于判断 task 数据量是否均衡。

---

## 4. 绘制 reward 分布图

对应函数：

```python
def plot_reward_distribution(df):
```

作用：

```text
查看所有 episode 的 reward 主要集中在哪些区间。
```

核心代码：

```python
reward_numeric = pd.to_numeric(df["reward"], errors="coerce")
valid_rewards = reward_numeric.dropna()
```

中文解释：

```text
pd.to_numeric(...)：把 reward 尽量转换成数字
errors="coerce"：如果 reward 不能转换成数字，就变成 NaN
dropna()：删除 NaN，只保留合法 reward 数值
```

例如原始 reward：

```text
8.5
3.2
bad
9.0
```

转换后：

```text
8.5
3.2
NaN
9.0
```

经过 `dropna()` 后：

```text
8.5
3.2
9.0
```

画图代码：

```python
plt.figure(figsize=(8, 5))

plt.hist(valid_rewards, bins=10)

plt.title("Reward Distribution")
plt.xlabel("Reward")
plt.ylabel("Episode Count")
plt.tight_layout()

plt.savefig(REWARD_DISTRIBUTION_FIGURE_PATH)
plt.close()
```

中文解释：

```text
plt.hist(...)：绘制直方图
valid_rewards：用于画图的 reward 数值
bins=10：把 reward 的范围分成 10 个区间
```

输出图片：

```text
results/figures/reward_distribution_v05.png
```

这张图回答的问题是：

```text
所有 episode 的 reward 整体分布怎么样？
```

可以帮助观察：

```text
1. reward 是否集中在高分区间
2. 是否有很多低 reward episode
3. reward 是否分布很散
4. 是否可能存在异常 reward
```

---

## 5. 绘制 task success rate 柱状图

对应函数：

```python
def plot_task_success_rate(df):
```

作用：

```text
按 task 分组，计算每个任务的成功率，并画成柱状图。
```

核心代码：

```python
success_numeric = pd.to_numeric(df["success"], errors="coerce")

df_success = df.copy()
df_success["success"] = success_numeric
df_success = df_success.dropna(subset=["success"])

task_success_rate = df_success.groupby("task")["success"].mean()
```

中文解释：

```text
success_numeric：把 success 尽量转换成数字
df.copy()：复制一份原始表，避免直接修改原始 df
df_success["success"] = success_numeric：用转换后的 success 替换原来的 success 列
dropna(subset=["success"])：只检查 success 列，删除 success 是 NaN 的行
groupby("task")：按 task 分组
["success"].mean()：计算每个 task 中 success 的平均值
```

因为：

```text
1 = 成功
0 = 失败
```

所以：

```text
success 的平均值 = success rate
```

例如：

```text
pick_cube 的 success 是：1, 0
平均值是：(1 + 0) / 2 = 0.5
所以 pick_cube 的 success rate 是 0.5
```

画图代码：

```python
plt.figure(figsize=(8, 5))

plt.bar(task_success_rate.index, task_success_rate.values)

plt.title("Success Rate by Task")
plt.xlabel("Task")
plt.ylabel("Success Rate")
plt.ylim(0, 1)
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(TASK_SUCCESS_RATE_FIGURE_PATH)
plt.close()
```

中文解释：

```text
task_success_rate.index：横轴，是 task 名称
task_success_rate.values：纵轴，是每个 task 的成功率
plt.ylim(0, 1)：把 y 轴范围固定为 0 到 1，因为成功率正常范围就是 0 到 1
```

输出图片：

```text
results/figures/task_success_rate_v05.png
```

这张图回答的问题是：

```text
每个任务做得好不好？
```

如果某个 task 的 success rate 很低，说明它可能是当前策略的短板。

---

## 6. 绘制 task average reward 柱状图

对应函数：

```python
def plot_task_average_reward(df):
```

作用：

```text
按 task 分组，计算每个任务的平均 reward，并画成柱状图。
```

核心代码：

```python
reward_numeric = pd.to_numeric(df["reward"], errors="coerce")

df_reward = df.copy()
df_reward["reward"] = reward_numeric
df_reward = df_reward.dropna(subset=["reward"])

task_average_reward = df_reward.groupby("task")["reward"].mean()
```

中文解释：

```text
reward_numeric：把 reward 尽量转换成数字
df.copy()：复制一份原始表
df_reward["reward"] = reward_numeric：用转换后的 reward 替换原 reward 列
dropna(subset=["reward"])：删除 reward 是 NaN 的行
groupby("task")：按 task 分组
["reward"].mean()：计算每个 task 的平均 reward
```

例如：

```text
pick_cube 的 reward 是：8.5, 3.2
平均 reward = (8.5 + 3.2) / 2 = 5.85
```

画图代码：

```python
plt.figure(figsize=(8, 5))

plt.bar(task_average_reward.index, task_average_reward.values)

plt.title("Average Reward by Task")
plt.xlabel("Task")
plt.ylabel("Average Reward")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(TASK_AVERAGE_REWARD_FIGURE_PATH)
plt.close()
```

输出图片：

```text
results/figures/task_average_reward_v05.png
```

这张图回答的问题是：

```text
不同任务的平均奖励表现怎么样？
```

它可以和 success rate 一起看：

```text
如果某个 task 成功率低，average reward 也低，说明它是明显短板。
如果某个 task 成功率高，但 average reward 不高，说明任务虽然完成了，但执行质量可能一般。
```

---

## 7. 为什么要把代码写成函数？

v0.5 最终脚本中使用了函数式结构：

```python
plot_task_episode_count(df)
plot_reward_distribution(df)
plot_task_success_rate(df)
plot_task_average_reward(df)
```

每个函数只负责一张图。

这样写的好处是：

```text
1. 代码结构更清楚
2. 每个功能相互独立
3. 后续想新增图片，只需要新增一个函数
4. main() 更简洁
5. 更接近真实项目代码风格
```

---

## 8. main() 函数

核心代码：

```python
def main():
    df = pd.read_csv(DATA_PATH)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plot_task_episode_count(df)
    plot_reward_distribution(df)
    plot_task_success_rate(df)
    plot_task_average_reward(df)

    print("\nAll v0.5 figures have been generated successfully.")
```

中文解释：

```text
df = pd.read_csv(DATA_PATH)：读取 data/episodes.csv
FIGURES_DIR.mkdir(...)：确保 results/figures 文件夹存在
plot_task_episode_count(df)：生成 task 数量图
plot_reward_distribution(df)：生成 reward 分布图
plot_task_success_rate(df)：生成 task 成功率图
plot_task_average_reward(df)：生成 task 平均 reward 图
```

---

## 9. v0.5 总结

v0.5 学习的重点是：

```text
把机器人 episode 数据分析结果可视化。
```

本阶段完成了 4 张图：

```text
1. task_episode_count_v05.png
2. reward_distribution_v05.png
3. task_success_rate_v05.png
4. task_average_reward_v05.png
```

相比 v0.4：

```text
v0.4 主要检查数据质量
v0.5 主要把数据指标画成图
```

v0.5 对应机器人数据闭环与评测岗位中的重要能力：

```text
不仅能计算指标，还能用可视化方式展示数据分布、任务表现和潜在问题。
```

本阶段掌握的核心能力包括：

```text
1. 使用 matplotlib 绘制柱状图
2. 使用 matplotlib 绘制直方图
3. 使用 value_counts() 统计任务数量
4. 使用 groupby("task") 计算任务级指标
5. 使用 pd.to_numeric() 清洗数值列
6. 使用 dropna() 去掉无效数据
7. 使用 savefig() 保存图片
8. 使用函数组织可视化代码
```
