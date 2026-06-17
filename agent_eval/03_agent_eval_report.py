"""
任务目标：
读取 Agent 任务轨迹数据，生成一份完整的 Agent 任务评测报告。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv；
2. 计算整体评测指标：task_count、success_rate、average_steps、average_score；
3. 筛选失败任务 badcase；
4. 统计 badcase_count 和 badcase_rate；
5. 统计 failure_reason 分布；
6. 按 task_type 分组统计任务表现；
7. 将结果保存到 results/agent_eval_report_v01.txt。

这个脚本对应 AI Agent 评测中的核心问题：
Agent 整体表现如何？哪些任务失败了？失败原因主要是什么？
"""

from pathlib import Path

import pandas as pd


# 1. 设置文件路径
# 用 __file__ 可以保证无论从哪里运行脚本，都能找到同文件夹下的 agent_tasks.csv
current_dir = Path(__file__).resolve().parent
csv_path = current_dir / "agent_tasks.csv"

# 报告统一保存到项目根目录的 results 文件夹
project_root = current_dir.parent
result_dir = project_root / "results"
result_dir.mkdir(exist_ok=True)

report_path = result_dir / "agent_eval_report_v01.txt"


# 2. 读取 Agent 任务轨迹数据
df = pd.read_csv(csv_path)


# 3. 计算整体基础指标
task_count = df.shape[0]
success_rate = df["success"].mean()
average_steps = df["steps"].mean()
average_score = df["final_score"].mean()


# 4. 筛选 badcase
# 当前定义：success = 0 的任务就是 badcase
badcases = df[df["success"] == 0]

badcase_count = badcases.shape[0]
badcase_rate = badcase_count / task_count


# 5. 统计失败原因分布
failure_reason_counts = badcases["failure_reason"].value_counts()


# 6. 按 task_type 分组统计
task_type_report = df.groupby("task_type").agg(
    task_count=("task_id", "count"),
    success_rate=("success", "mean"),
    average_steps=("steps", "mean"),
    average_score=("final_score", "mean")
)


# 7. 写入报告文件
with open(report_path, "w", encoding="utf-8") as f:
    f.write("Agent Task Evaluation Report v0.1\n")
    f.write("=" * 60 + "\n\n")

    f.write("1. Overall Evaluation\n")
    f.write("-" * 60 + "\n")
    f.write(f"task_count: {task_count}\n")
    f.write(f"success_rate: {success_rate:.4f}\n")
    f.write(f"average_steps: {average_steps:.4f}\n")
    f.write(f"average_score: {average_score:.4f}\n\n")

    f.write("2. Badcase Summary\n")
    f.write("-" * 60 + "\n")
    f.write(f"badcase_count: {badcase_count}\n")
    f.write(f"badcase_rate: {badcase_rate:.4f}\n\n")

    f.write("3. Failure Reason Distribution\n")
    f.write("-" * 60 + "\n")
    if badcase_count > 0:
        f.write(failure_reason_counts.to_string())
        f.write("\n\n")
    else:
        f.write("No badcases found.\n\n")

    f.write("4. Task Type Evaluation\n")
    f.write("-" * 60 + "\n")
    f.write(task_type_report.to_string())
    f.write("\n\n")

    f.write("5. Badcase Details\n")
    f.write("-" * 60 + "\n")

    if badcase_count > 0:
        for _, row in badcases.iterrows():
            f.write(
                f"task_id: {row['task_id']} | "
                f"task_type: {row['task_type']} | "
                f"steps: {row['steps']} | "
                f"failure_reason: {row['failure_reason']} | "
                f"task: {row['task']}\n"
            )
    else:
        f.write("No badcase details.\n")


# 8. 在终端提示报告保存位置
print("Agent evaluation report has been generated successfully.")
print("Report path:", report_path)