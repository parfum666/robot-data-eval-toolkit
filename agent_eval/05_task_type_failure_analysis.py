"""
任务目标：
按 task_type 分析 Agent 任务表现，找出哪类任务更容易失败。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv;
2. 按 task_type 分组统计任务数量；
3. 按 task_type 统计 success_rate;
4. 计算每类任务的 failure_rate ;
5. 统计每类任务的 average_steps 和 average_score ;
6. 找出 failure_rate 最高的任务类型。

这个脚本对应 AI Agent 评测中的核心问题：
Agent 在哪些类型的任务上表现较差？
"""

from pathlib import Path

import pandas as pd


# 1. 设置 CSV 文件路径
# 当前脚本位于 agent_eval/ 文件夹中
# agent_tasks.csv 也位于同一个 agent_eval/ 文件夹中
current_dir = Path(__file__).resolve().parent
csv_path = current_dir / "agent_tasks.csv"


# 2. 读取 Agent 任务轨迹数据
df = pd.read_csv(csv_path)

task_type_report = df.groupby("task").agg(
    task_count=("task_id", "count"),
    success_rate=("success", "mean"),
    average_steps=("steps", "mean"),
    average_score=("final_score", "mean")
)
task_type_report["failure_rate"] = 1 - task_type_report["success_rate"]
# 5. 按 failure_rate 从高到低排序
task_type_report = task_type_report.sort_values(
    by= "failure_rate",
    ascending=False
)

most_failed_task_type = task_type_report.index[0]
highest_failure_rate = task_type_report.iloc[0]["failure_rate"]


# 7. 输出 task_type 维度评测结果
print("Agent Task Type Failure Analysis")
print("--------------------------------")
print(task_type_report)


# 8. 输出最容易失败的任务类型
print("\nMost Failed Task Type")
print("--------------------------------")
print("task_type:", most_failed_task_type)
print("failure_rate:", highest_failure_rate)