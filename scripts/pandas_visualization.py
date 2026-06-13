from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# v0.5 Pandas Data Visualization
# =========================================================
# 功能：
# 1. 绘制每个 task 的 episode 数量柱状图
# 2. 绘制 reward 分布直方图
# 3. 绘制每个 task 的 success rate 柱状图
# 4. 绘制每个 task 的 average reward 柱状图
# =========================================================


DATA_PATH = Path("data") / "episodes.csv"

FIGURES_DIR = Path("results") / "figures"

TASK_COUNT_FIGURE_PATH = FIGURES_DIR / "task_episode_count_v05.png"
REWARD_DISTRIBUTION_FIGURE_PATH = FIGURES_DIR / "reward_distribution_v05.png"
TASK_SUCCESS_RATE_FIGURE_PATH = FIGURES_DIR / "task_success_rate_v05.png"
TASK_AVERAGE_REWARD_FIGURE_PATH = FIGURES_DIR / "task_average_reward_v05.png"


def plot_task_episode_count(df):
    """
    绘制每个 task 的 episode 数量柱状图。

    作用：
    查看不同任务的数据量是否均衡。
    """

    # 统计每个 task 出现了多少次
    task_counts = df["task"].value_counts()

    print("Task Episode Count")
    print("--------------------------------")
    print(task_counts)

    # 创建图像
    plt.figure(figsize=(8, 5))

    # 横轴：task 名称
    # 纵轴：每个 task 的 episode 数量
    plt.bar(task_counts.index, task_counts.values)

    plt.title("Episode Count by Task")
    plt.xlabel("Task")
    plt.ylabel("Episode Count")
    plt.xticks(rotation=30)
    plt.tight_layout()

    # 保存图片
    plt.savefig(TASK_COUNT_FIGURE_PATH)

    # 关闭当前图，避免影响下一张图
    plt.close()

    print(f"Figure saved to: {TASK_COUNT_FIGURE_PATH}")


def plot_reward_distribution(df):
    """
    绘制 reward 分布直方图。

    作用：
    查看所有 episode 的 reward 主要集中在哪些区间。
    """

    # 把 reward 尽量转换成数字
    # 不能转换的值会变成 NaN
    reward_numeric = pd.to_numeric(df["reward"], errors="coerce")

    # 删除 NaN，只保留合法 reward 数值
    valid_rewards = reward_numeric.dropna()

    print("\nReward Summary")
    print("--------------------------------")
    print(valid_rewards.describe())

    plt.figure(figsize=(8, 5))

    # 绘制 reward 分布直方图
    # bins=10 表示把 reward 范围分成 10 个区间
    plt.hist(valid_rewards, bins=10)

    plt.title("Reward Distribution")
    plt.xlabel("Reward")
    plt.ylabel("Episode Count")
    plt.tight_layout()

    plt.savefig(REWARD_DISTRIBUTION_FIGURE_PATH)
    plt.close()

    print(f"Figure saved to: {REWARD_DISTRIBUTION_FIGURE_PATH}")


def plot_task_success_rate(df):
    """
    绘制每个 task 的 success rate 柱状图。

    作用：
    查看每个任务的成功率。
    """

    # 把 success 尽量转换成数字
    # 非数字 success 会变成 NaN
    success_numeric = pd.to_numeric(df["success"], errors="coerce")

    # 复制一份 df，避免直接修改原始数据
    df_success = df.copy()

    # 用转换后的 success 替换原 success 列
    df_success["success"] = success_numeric

    # 删除 success 是 NaN 的行
    df_success = df_success.dropna(subset=["success"])

    # 按 task 分组，计算每个任务的 success 平均值
    # 因为 1 表示成功，0 表示失败，所以 mean() 就是成功率
    task_success_rate = df_success.groupby("task")["success"].mean()

    print("\nTask Success Rate")
    print("--------------------------------")
    print(task_success_rate)

    plt.figure(figsize=(8, 5))

    # 横轴：task 名称
    # 纵轴：每个 task 的成功率
    plt.bar(task_success_rate.index, task_success_rate.values)

    plt.title("Success Rate by Task")
    plt.xlabel("Task")
    plt.ylabel("Success Rate")

    # success rate 正常范围是 0 到 1
    plt.ylim(0, 1)

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(TASK_SUCCESS_RATE_FIGURE_PATH)
    plt.close()

    print(f"Figure saved to: {TASK_SUCCESS_RATE_FIGURE_PATH}")


def plot_task_average_reward(df):
    """
    绘制每个 task 的 average reward 柱状图。

    作用：
    查看每个任务的平均奖励表现。
    """

    # 把 reward 尽量转换成数字
    reward_numeric = pd.to_numeric(df["reward"], errors="coerce")

    # 复制一份 df，避免直接修改原始数据
    df_reward = df.copy()

    # 用转换后的 reward 替换原 reward 列
    df_reward["reward"] = reward_numeric

    # 删除 reward 是 NaN 的行
    df_reward = df_reward.dropna(subset=["reward"])

    # 按 task 分组，计算每个任务的平均 reward
    task_average_reward = df_reward.groupby("task")["reward"].mean()

    print("\nTask Average Reward")
    print("--------------------------------")
    print(task_average_reward)

    plt.figure(figsize=(8, 5))

    # 横轴：task 名称
    # 纵轴：每个 task 的平均 reward
    plt.bar(task_average_reward.index, task_average_reward.values)

    plt.title("Average Reward by Task")
    plt.xlabel("Task")
    plt.ylabel("Average Reward")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(TASK_AVERAGE_REWARD_FIGURE_PATH)
    plt.close()

    print(f"Figure saved to: {TASK_AVERAGE_REWARD_FIGURE_PATH}")


def main():
    # 读取 episode 数据
    df = pd.read_csv(DATA_PATH)

    # 确保 results/figures 文件夹存在
    # parents=True 表示如果 results 也不存在，就一起创建
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # 依次生成 4 张图
    plot_task_episode_count(df)
    plot_reward_distribution(df)
    plot_task_success_rate(df)
    plot_task_average_reward(df)

    print("\nAll v0.5 figures have been generated successfully.")


if __name__ == "__main__":
    main()