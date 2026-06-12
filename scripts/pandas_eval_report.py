from pathlib import Path

import pandas as pd


# =========================================================
# v0.3 Final: Generate Pandas robot episode evaluation report
# =========================================================
# 功能：
# 1. 读取 data/episodes.csv
# 2. 计算整体 episode 指标
# 3. 按 task 分组统计指标
# 4. 筛选失败 episode
# 5. 统计失败 episode 的 task 分布
# 6. 生成 results/pandas_eval_report_v03.txt
# =========================================================


DATA_PATH = Path("data") / "episodes.csv"
RESULTS_DIR = Path("results")
REPORT_PATH = RESULTS_DIR / "pandas_eval_report_v03.txt"


def main():
    # 1. 读取 episode 数据
    df = pd.read_csv(DATA_PATH)

    # 2. 整体评测指标
    total_episode_count = df.shape[0]
    average_reward = df["reward"].mean()
    success_rate = df["success"].mean()
    average_steps = df["steps"].mean()

    # 3. 按 task 分组统计
    task_report = df.groupby("task").agg(
        episode_count = ("episode_id","count"),
        average_reward=("reward", "mean"),
        success_rate=("success", "mean"),
        average_steps=("steps", "mean"),
    )

    task_report = task_report.round(4)

    # 4. 筛选失败 episode
    failed_episodes = df[df["success"] == 0]
    failed_count = failed_episodes.shape[0]

    if total_episode_count == 0:
        failed_rate = 0
    else:
        failed_rate = failed_count / total_episode_count

    # 5. 统计失败 episode 的 task 分布
    failed_task_counts = failed_episodes["task"].value_counts()

    # 6. 组织报告内容
    report_lines = [
        "Pandas Robot Episode Evaluation Report v0.3",
        "================================================",
        "",
        "Overall Evaluation",
        "------------------------------------------------",
        f"Total episode count: {total_episode_count}",
        f"Average reward: {round(average_reward, 4)}",
        f"Success rate: {round(success_rate, 4)}",
        f"Average steps: {round(average_steps, 4)}",
        "",
        "Task-level Evaluation Report",
        "------------------------------------------------",
        task_report.to_string(),
        "",
        "Failed Episodes",
        "------------------------------------------------",
    ]

    if failed_count == 0:
        report_lines.append("No failed episodes.")
    else:
        report_lines.append(failed_episodes.to_string(index=False))

    report_lines.extend(
        [
            "",
            "Failure Summary",
            "------------------------------------------------",
            f"Failed episode count: {failed_count}",
            f"Failed rate: {round(failed_rate, 4)}",
            "",
            "Failed Episode Count by Task",
            "------------------------------------------------",
        ]
    )

    if failed_count == 0:
        report_lines.append("No failed tasks.")
    else:
        report_lines.append(failed_task_counts.to_string())

    report_text = "\n".join(report_lines)

    # 7. 保存报告
    report_path = Path("results") / "pandas_eval_report_v03.txt"
    with open (report_path , "w",encoding="utf-8") as file:
        file.write(report_text)

    # 8. 同时打印到终端
    print(report_text)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()