"""
任务目标：
生成 Agent 任务评测完整报告 v02。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv；
2. 计算整体评测指标；
3. 统计 badcase 和 failure_reason 分布；
4. 分析 tool_calls 工具调用情况；
5. 按 task_type 分析不同任务类型表现；
6. 分析 long-horizon task 的失败情况；
7. 将完整评测结果保存到 results/agent_eval_report_v02.txt。

这个脚本对应 AI Agent 评测岗位中的核心能力：
从任务轨迹数据中分析 Agent 的整体表现、失败样本、失败原因、工具调用风险和长时序任务表现。
"""

from pathlib import Path

import pandas as pd


# 1. 设置文件路径
# 当前脚本位于 agent_eval/ 文件夹中
current_dir = Path(__file__).resolve().parent

# agent_tasks.csv 与当前脚本在同一个文件夹中
csv_path = current_dir / "agent_tasks.csv"

# 项目根目录是 agent_eval 的上一层
project_root = current_dir.parent

# 报告保存到项目根目录下的 results 文件夹
result_dir = project_root / "results"
result_dir.mkdir(exist_ok=True)

report_path = result_dir / "agent_eval_report_v02.txt"


# 2. 读取 Agent 任务轨迹数据
df = pd.read_csv(csv_path)


# 3. 基础评测指标
task_count = df.shape[0]
success_rate = df["success"].mean()
average_steps = df["steps"].mean()
average_score = df["final_score"].mean()


# 4. badcase 分析
badcases = df[df["success"] == 0]

badcase_count = badcases.shape[0]
badcase_rate = badcase_count / task_count

failure_reason_counts = badcases["failure_reason"].value_counts()


# 5. tool_calls 工具调用分析
# 将工具调用字符串拆成列表
df["tool_call_list"] = df["tool_calls"].apply(lambda x: str(x).split("|"))

# 统计每条任务调用了几个工具
df["tool_call_count"] = df["tool_call_list"].apply(len)

average_tool_calls = df["tool_call_count"].mean()

success_tasks = df[df["success"] == 1]
failed_tasks = df[df["success"] == 0]

success_average_tool_calls = success_tasks["tool_call_count"].mean()
failed_average_tool_calls = failed_tasks["tool_call_count"].mean()

# 统计所有工具使用频率
all_tools = df["tool_call_list"].explode()
tool_counts = all_tools.value_counts()

# 统计失败任务中的工具使用频率
failed_tools = failed_tasks["tool_call_list"].explode()
failed_tool_counts = failed_tools.value_counts()

# 筛选工具调用错误任务
tool_call_error_tasks = df[df["failure_reason"] == "tool_call_error"]


# 6. task_type 维度分析
task_type_report = df.groupby("task_type").agg(
    task_count=("task_id", "count"),
    success_rate=("success", "mean"),
    average_steps=("steps", "mean"),
    average_score=("final_score", "mean"),
    average_tool_calls=("tool_call_count", "mean")
)

task_type_report["failure_rate"] = 1 - task_type_report["success_rate"]

task_type_report = task_type_report.sort_values(
    by="failure_rate",
    ascending=False
)

most_failed_task_type = task_type_report.index[0]
highest_failure_rate = task_type_report.iloc[0]["failure_rate"]


# 7. long-horizon 长时序任务分析
# 当前 demo 中，steps >= 6 的任务定义为 long-horizon task
long_horizon_tasks = df[df["steps"] >= 6]

long_horizon_count = long_horizon_tasks.shape[0]
long_horizon_success_rate = long_horizon_tasks["success"].mean()
long_horizon_failure_rate = 1 - long_horizon_success_rate

long_horizon_badcases = long_horizon_tasks[long_horizon_tasks["success"] == 0]

success_average_steps = success_tasks["steps"].mean()
failed_average_steps = failed_tasks["steps"].mean()


# 8. 写入完整报告
with open(report_path, "w", encoding="utf-8") as f:
    f.write("Agent Task Evaluation Report v02\n")
    f.write("=" * 70 + "\n\n")

    f.write("1. Overall Evaluation\n")
    f.write("-" * 70 + "\n")
    f.write(f"task_count: {task_count}\n")
    f.write(f"success_rate: {success_rate:.4f}\n")
    f.write(f"average_steps: {average_steps:.4f}\n")
    f.write(f"average_score: {average_score:.4f}\n\n")

    f.write("2. Badcase Summary\n")
    f.write("-" * 70 + "\n")
    f.write(f"badcase_count: {badcase_count}\n")
    f.write(f"badcase_rate: {badcase_rate:.4f}\n\n")

    f.write("3. Failure Reason Distribution\n")
    f.write("-" * 70 + "\n")
    if badcase_count > 0:
        f.write(failure_reason_counts.to_string())
        f.write("\n\n")
    else:
        f.write("No badcases found.\n\n")

    f.write("4. Tool Call Analysis\n")
    f.write("-" * 70 + "\n")
    f.write(f"average_tool_calls: {average_tool_calls:.4f}\n")
    f.write(f"success_average_tool_calls: {success_average_tool_calls:.4f}\n")
    f.write(f"failed_average_tool_calls: {failed_average_tool_calls:.4f}\n\n")

    f.write("Tool Usage Frequency:\n")
    f.write(tool_counts.to_string())
    f.write("\n\n")

    f.write("Tool Usage Frequency in Failed Tasks:\n")
    if failed_tool_counts.shape[0] > 0:
        f.write(failed_tool_counts.to_string())
        f.write("\n\n")
    else:
        f.write("No failed tool calls found.\n\n")

    f.write("5. Tool Call Error Tasks\n")
    f.write("-" * 70 + "\n")
    if tool_call_error_tasks.shape[0] > 0:
        for _, row in tool_call_error_tasks.iterrows():
            f.write(
                f"task_id: {row['task_id']} | "
                f"task_type: {row['task_type']} | "
                f"tool_calls: {row['tool_calls']} | "
                f"failure_reason: {row['failure_reason']} | "
                f"task: {row['task']}\n"
            )
        f.write("\n")
    else:
        f.write("No tool_call_error tasks found.\n\n")

    f.write("6. Task Type Evaluation\n")
    f.write("-" * 70 + "\n")
    f.write(task_type_report.to_string())
    f.write("\n\n")

    f.write("Most Failed Task Type:\n")
    f.write(f"task_type: {most_failed_task_type}\n")
    f.write(f"failure_rate: {highest_failure_rate:.4f}\n\n")

    f.write("7. Long-horizon Task Analysis\n")
    f.write("-" * 70 + "\n")
    f.write(f"success_average_steps: {success_average_steps:.4f}\n")
    f.write(f"failed_average_steps: {failed_average_steps:.4f}\n")
    f.write(f"long_horizon_count: {long_horizon_count}\n")
    f.write(f"long_horizon_success_rate: {long_horizon_success_rate:.4f}\n")
    f.write(f"long_horizon_failure_rate: {long_horizon_failure_rate:.4f}\n\n")

    f.write("Long-horizon Badcase Details:\n")
    if long_horizon_badcases.shape[0] > 0:
        for _, row in long_horizon_badcases.iterrows():
            f.write(
                f"task_id: {row['task_id']} | "
                f"task_type: {row['task_type']} | "
                f"steps: {row['steps']} | "
                f"tool_call_count: {row['tool_call_count']} | "
                f"failure_reason: {row['failure_reason']} | "
                f"task: {row['task']}\n"
            )
    else:
        f.write("No long-horizon badcases found.\n")

    f.write("\n")

    f.write("8. Badcase Details\n")
    f.write("-" * 70 + "\n")
    if badcase_count > 0:
        for _, row in badcases.iterrows():
            f.write(
                f"task_id: {row['task_id']} | "
                f"task_type: {row['task_type']} | "
                f"steps: {row['steps']} | "
                f"tool_calls: {row['tool_calls']} | "
                f"failure_reason: {row['failure_reason']} | "
                f"task: {row['task']}\n"
            )
    else:
        f.write("No badcase details.\n")


# 9. 在终端输出提示
print("Agent evaluation report v02 has been generated successfully.")
print("Report path:", report_path)