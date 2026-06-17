from pathlib import Path
import pandas as pd

"""
任务目标：
分析 Agent 任务轨迹中的工具调用情况。

本脚本用于完成：
1. 读取 agent_eval/agent_tasks.csv
2. 统计每条任务调用了多少个工具；
3. 对比成功任务和失败任务的平均工具调用次数；
4. 统计所有工具的使用频率；
5. 统计失败任务中出现过哪些工具；
6. 判断 tool_call_error 是否与工具调用有关。

这个脚本对应 AI Agent 评测中的核心问题：
Agent 的失败是否和工具调用过程有关？
"""

current_dir = Path(__file__).resolve().parent
csv_path = current_dir / "agent_tasks.csv"

df = pd.read_csv(csv_path)

df["tool_call_list"] = df["tool_calls"].apply(lambda x:str(x).split("|"))
# 4. 统计每条任务调用了几个工具
df["tool_call_count"] = df["tool_calls"].apply(len)
# 5. 计算整体平均工具调用次数
average_tool_calls = df["tool_call_count"].mean()

success_tasks = df[df["success"] == 1]
failed_tasks = df[df["success"] == 0]

success_average_tool_calls = success_tasks["tool_call_count"].mean()
failed_average_tool_calls = failed_tasks["tool_call_count"].mean()

# 7. 统计所有工具出现频率
all_tools = df["tool_call_list"].explode()
tool_counts = all_tools.value_counts()

failed_tools = failed_tasks["tool_call_list"].explode()
failed_tool_counts = failed_tools.value_counts()

# 9. 筛选工具调用错误的任务
tool_call_error_tasks = df[df["failure_reason"] == "tool_call_error"]

print("Agent Tool Call Analysis")
print("--------------------------------")
print("task_count:", df.shape[0])
print("average_tool_calls:", average_tool_calls)
print("success_average_tool_calls:", success_average_tool_calls)
print("failed_average_tool_calls:", failed_average_tool_calls)


print("\nTool Usage Frequency")
print("--------------------------------")
print(tool_counts)


print("\nTool Usage Frequency in Failed Tasks")
print("--------------------------------")
print(failed_tool_counts)


print("\nTool Call Error Tasks")
print("--------------------------------")

if tool_call_error_tasks.shape[0] > 0:
    for _, row in tool_call_error_tasks.iterrows():
        print(
            "task_id:", row["task_id"],
            "| task_type:", row["task_type"],
            "| tool_calls:", row["tool_calls"],
            "| failure_reason:", row["failure_reason"],
            "| task:", row["task"]
        )
else:
    print("No tool_call_error tasks found.")


