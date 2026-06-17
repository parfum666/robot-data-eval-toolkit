"""
任务目标：
读取 Agent 任务轨迹数据，并计算基础评测指标。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv；
2. 统计 Agent 任务总数；
3. 计算任务成功率 success_rate；
4. 计算平均执行步数 average_steps；
5. 计算平均任务得分 average_score。

这个脚本对应 AI Agent 评测中的基础问题：
Agent 完成任务的整体表现怎么样？
"""

from pathlib import Path

import pandas as pd


# 1. 设置 CSV 文件路径
csv_path = Path("agent_eval") / "agent_tasks.csv"


# 2. 读取 Agent 任务轨迹数据
df = pd.read_csv(csv_path)


# 3. 查看数据基本信息
print("Agent Task Data Preview")
print("--------------------------------")
print(df.head())

print("\nData Shape")
print("--------------------------------")
print("rows:", df.shape[0])
print("columns:", df.shape[1])


# 4. 计算任务总数
task_count = df.shape[0]


# 5. 计算任务成功率
# success 列中，1 表示成功，0 表示失败
# 因此 success 的平均值就是成功率
success_rate = df["success"].mean()


# 6. 计算平均执行步数
average_steps = df["steps"].mean()


# 7. 计算平均任务得分
average_score = df["final_score"].mean()


# 8. 输出整体评测结果
print("\nAgent Evaluation Metrics")
print("--------------------------------")
print("task_count:", task_count)
print("success_rate:", success_rate)
print("average_steps:", average_steps)
print("average_score:", average_score)