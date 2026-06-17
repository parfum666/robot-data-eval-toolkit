"""
任务目标：
分析 Agent 长时序任务和多工具调用任务是否更容易失败。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv；
2. 统计成功任务和失败任务的平均 steps；
3. 统计成功任务和失败任务的平均 tool_call_count；
4. 定义 long_horizon_task：steps >= 6 的任务；
5. 统计 long_horizon_task 的成功率和失败率；
6. 输出长时序任务中的 badcase。

这个脚本对应 AI Agent 评测中的核心问题：
Agent 在步骤较长、工具链较长的任务中是否更容易失败？
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
# 3. 将 tool_calls 字符串拆成工具列表
df["tool_call_list"] = df["tool_calls"].apply(lambda x : str(x).split("|"))

# 4. 统计每条任务的工具调用次数
df["tool_call_count"]= df["tool_calls"].apply(len)

# 5. 分别筛选成功任务和失败任务
success_tasks = df[df["success"] == 1]
failed_tasks = df[df["success"] == 0]

success_average_tool_calls = success_tasks["tool_call_count"].mean()
failed_average_tool_calls = failed_tasks["tool_call_count"].mean()


# 7. 对比成功任务和失败任务的平均工具调用次数

success_average_steps = success_tasks["steps"].mean()
failed_average_steps = failed_tasks["steps"].mean()

# 8. 定义长时序任务
# 这里先简单规定：steps >= 6 的任务就是 long-horizon task
long_horizon_tasks = df[df["steps"] >= 6]


# 9. 统计长时序任务数量、成功率和失败率

long_horizon_count = long_horizon_tasks.shape[0]
long_horizon_success_rate = long_horizon_tasks["success"].mean()
long_horizon_failure_rate = 1 - long_horizon_success_rate


# 10. 筛选长时序任务中的 badcase

long_horizon_badcases = long_horizon_tasks[long_horizon_tasks["success"] == 0]

print("Agent Long-horizon Failure Analysis")
print("--------------------------------")
print("success_average_steps:", success_average_steps)
print("failed_average_steps:", failed_average_steps)
print("success_average_tool_calls:", success_average_tool_calls)
print("failed_average_tool_calls:", failed_average_tool_calls)

print("\nLong-horizon Task Summary")
print("--------------------------------")
print("long_horizon_count:", long_horizon_count)
print("long_horizon_success_rate:", long_horizon_success_rate)
print("long_horizon_failure_rate:", long_horizon_failure_rate)

print("\nLong-horizon Badcase Details")
print("--------------------------------")

if long_horizon_badcases.shape[0] > 0:
    for _, row in long_horizon_badcases.iterrows():
        print(
            "task_id:", row["task_id"],
            "| task_type:", row["task_type"],
            "| steps:", row["steps"],
            "| tool_call_count:", row["tool_call_count"],
            "| failure_reason:", row["failure_reason"],
            "| task:", row["task"]
        )
else:
    print("No long-horizon badcases found.")

