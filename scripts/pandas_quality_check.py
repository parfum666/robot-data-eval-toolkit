from pathlib import Path

import pandas as pd


# =========================================================
# v0.4 Data Quality Check for Robot Episode Data
# =========================================================
# 功能：
# 1. 检查必要字段是否存在
# 2. 检查缺失值
# 3. 检查 success 标签是否合法
# 4. 检查 reward 是否异常
# 5. 检查 steps 是否异常
# 6. 检查 episode_id 是否重复
# 7. 检查 episode_id 是否连续
# 8. 检查 task 数据量是否均衡
# =========================================================


DATA_PATH = Path("data") / "episodes.csv"
RESULTS_DIR = Path("results")
REPORT_PATH = RESULTS_DIR / "data_quality_report_v04.txt"


# 机器人 episode 数据中必须存在的字段
REQUIRED_COLUMNS = [
    "episode_id",
    "task",
    "reward",
    "success",
    "steps",
]


# reward 的合理范围
# 当前 toy project 中暂定 reward 应该在 [0, 100] 之间
REWARD_MIN = 0
REWARD_MAX = 100


# steps 的合理范围
# steps 表示执行步数，通常应该是正整数
STEPS_MIN = 1
STEPS_MAX = 1000


# task 数据量检查参数
# 每个 task 至少希望有 2 条 episode
TASK_MIN_COUNT = 2

# 如果最多 task 的数量 / 最少 task 的数量 超过 3，就认为任务分布不均衡
TASK_IMBALANCE_RATIO = 3.0


def main():
    # =====================================================
    # Part 0: 读取数据
    # =====================================================

    df = pd.read_csv(DATA_PATH)

    print("First 5 rows:")
    print(df.head())

    print("\nDataFrame columns:")
    print(df.columns)

    # =====================================================
    # Part 1: 检查必要字段是否存在
    # =====================================================

    missing_columns = []

    for col in REQUIRED_COLUMNS:
        # 判别逻辑：
        # 如果某个必需字段不在 df.columns 里面，说明 CSV 缺少这个字段
        if col not in df.columns:
            missing_columns.append(col)

    print("\nRequired Column Check")
    print("--------------------------------")

    if len(missing_columns) == 0:
        print("All required columns exist.")
    else:
        print("Missing required columns:")
        print(missing_columns)

        # 如果关键字段缺失，后面的分析没有意义，直接结束程序
        return

    # =====================================================
    # Part 2: 检查缺失值
    # =====================================================

    # df.isna() 会检查每个格子是否为空
    # .sum() 会统计每一列有多少个缺失值
    missing_value_summary = df.isna().sum()

    print("\nMissing Value Summary")
    print("--------------------------------")
    print(missing_value_summary)

    # 判别逻辑：
    # df.isna().any(axis=1) 表示只要某一行有任意一个缺失值，就标记为 True
    # df[...] 会把这些存在缺失值的行筛选出来
    episodes_with_missing_values = df[df.isna().any(axis=1)]

    missing_episode_count = episodes_with_missing_values.shape[0]
    total_episode_count = df.shape[0]

    if total_episode_count == 0:
        missing_episode_rate = 0
    else:
        missing_episode_rate = missing_episode_count / total_episode_count

    print("\nEpisodes with Missing Values")
    print("--------------------------------")

    if missing_episode_count == 0:
        print("No episodes with missing values.")
    else:
        print(episodes_with_missing_values)

    print("\nMissing Value Check Summary")
    print("--------------------------------")
    print(f"Total episode count: {total_episode_count}")
    print(f"Episodes with missing values: {missing_episode_count}")
    print(f"Missing episode rate: {round(missing_episode_rate, 4)}")

    # =====================================================
    # Part 3: 检查 success 标签是否合法
    # =====================================================

    # 把 success 尽量转换成数字
    # 如果遇到 yes、no、abc 这种不能转成数字的内容，会变成 NaN
    success_numeric = pd.to_numeric(df["success"], errors="coerce")

    # 判别逻辑：
    # 1. df["success"].notna()：原始 success 不是空值
    # 2. success_numeric.isin([0, 1])：转换后的 success 是否属于 0 或 1
    # 3. ~ 表示取反，也就是“不属于 0 或 1”
    # 所以这里筛选的是：success 非空，但不是合法标签 0/1 的 episode
    invalid_success_episodes = df[
        df["success"].notna() & (~success_numeric.isin([0, 1]))
    ]

    invalid_success_count = invalid_success_episodes.shape[0]

    if total_episode_count == 0:
        invalid_success_rate = 0
    else:
        invalid_success_rate = invalid_success_count / total_episode_count

    print("\nInvalid Success Label Episodes")
    print("--------------------------------")

    if invalid_success_count == 0:
        print("All success labels are valid.")
    else:
        print(invalid_success_episodes)

    print("\nSuccess Label Check Summary")
    print("--------------------------------")
    print(f"Invalid success label count: {invalid_success_count}")
    print(f"Invalid success label rate: {round(invalid_success_rate, 4)}")

    # =====================================================
    # Part 4: 检查 reward 是否异常
    # =====================================================

    # 把 reward 尽量转换成数字
    # bad、abc 这种非数字 reward 会变成 NaN
    reward_numeric = pd.to_numeric(df["reward"], errors="coerce")

    # 判别逻辑：
    # 1. df["reward"].notna()：原始 reward 不是空值
    # 2. reward_numeric.isna()：原始 reward 非空，但转换成数字失败
    # 3. reward_numeric < REWARD_MIN：reward 小于合理下限
    # 4. reward_numeric > REWARD_MAX：reward 大于合理上限
    # 满足任意一种异常，都筛选出来
    invalid_reward_episodes = df[
        df["reward"].notna()
        & (
            reward_numeric.isna()
            | (reward_numeric < REWARD_MIN)
            | (reward_numeric > REWARD_MAX)
        )
    ]

    invalid_reward_count = invalid_reward_episodes.shape[0]

    if total_episode_count == 0:
        invalid_reward_rate = 0
    else:
        invalid_reward_rate = invalid_reward_count / total_episode_count

    print("\nInvalid Reward Episodes")
    print("--------------------------------")

    if invalid_reward_count == 0:
        print("All reward values are valid.")
    else:
        print(invalid_reward_episodes)

    print("\nReward Check Summary")
    print("--------------------------------")
    print(f"Reward valid range: [{REWARD_MIN}, {REWARD_MAX}]")
    print(f"Invalid reward count: {invalid_reward_count}")
    print(f"Invalid reward rate: {round(invalid_reward_rate, 4)}")

    # =====================================================
    # Part 5: 检查 steps 是否异常
    # =====================================================

    # 把 steps 尽量转换成数字
    # bad、abc 这种非数字 steps 会变成 NaN
    steps_numeric = pd.to_numeric(df["steps"], errors="coerce")

    # 判别逻辑：
    # steps 表示步数，应该是整数
    # steps_numeric % 1 != 0 表示这个数不是整数，例如 42.5
    # steps_numeric.notna() 是为了只对成功转换成数字的值做整数检查
    steps_is_not_integer = steps_numeric.notna() & (steps_numeric % 1 != 0)

    # 判别逻辑：
    # 1. 原始 steps 非空
    # 2. steps 转数字失败，或者小于最小步数，或者大于最大步数，或者不是整数
    invalid_steps_episodes = df[
        df["steps"].notna()
        & (
            steps_numeric.isna()
            | (steps_numeric < STEPS_MIN)
            | (steps_numeric > STEPS_MAX)
            | steps_is_not_integer
        )
    ]

    invalid_steps_count = invalid_steps_episodes.shape[0]

    if total_episode_count == 0:
        invalid_steps_rate = 0
    else:
        invalid_steps_rate = invalid_steps_count / total_episode_count

    print("\nInvalid Steps Episodes")
    print("--------------------------------")

    if invalid_steps_count == 0:
        print("All steps values are valid.")
    else:
        print(invalid_steps_episodes)

    print("\nSteps Check Summary")
    print("--------------------------------")
    print(f"Steps valid range: [{STEPS_MIN}, {STEPS_MAX}]")
    print(f"Invalid steps count: {invalid_steps_count}")
    print(f"Invalid steps rate: {round(invalid_steps_rate, 4)}")

    # =====================================================
    # Part 6: 检查 episode_id 是否重复
    # =====================================================

    # 把 episode_id 尽量转换成数字
    # 后面检查连续性时会用到
    episode_id_numeric = pd.to_numeric(df["episode_id"], errors="coerce")

    # 判别逻辑：
    # duplicated(keep=False) 会把所有重复的 episode_id 都标记为 True
    # keep=False 的意思是：只要这个 id 重复出现，所有相关行都筛出来
    duplicated_episode_id_episodes = df[
        df["episode_id"].duplicated(keep=False)
    ]

    duplicated_episode_id_count = duplicated_episode_id_episodes.shape[0]

    print("\nDuplicated Episode ID Episodes")
    print("--------------------------------")

    if duplicated_episode_id_count == 0:
        print("No duplicated episode_id.")
    else:
        print(duplicated_episode_id_episodes)

    print("\nEpisode ID Duplicate Check Summary")
    print("--------------------------------")
    print(f"Duplicated episode_id row count: {duplicated_episode_id_count}")

    # =====================================================
    # Part 7: 检查 episode_id 是否连续
    # =====================================================

    # 判别逻辑：
    # 1. episode_id_numeric.notna()：episode_id 成功转换成了数字
    # 2. episode_id_numeric % 1 == 0：episode_id 是整数
    # 3. astype(int)：把 1.0、2.0 转成 1、2
    valid_episode_ids = episode_id_numeric[
        episode_id_numeric.notna() & (episode_id_numeric % 1 == 0)
    ].astype(int)

    # 去重并排序
    unique_episode_ids = sorted(valid_episode_ids.unique())

    if len(unique_episode_ids) == 0:
        missing_episode_ids = []
    else:
        # 当前项目默认 episode_id 应该从 1 开始连续递增
        # expected_episode_ids 是理论上应该存在的 id 集合
        expected_episode_ids = set(range(1, max(unique_episode_ids) + 1))

        # actual_episode_ids 是当前数据中实际存在的 id 集合
        actual_episode_ids = set(unique_episode_ids)

        # 判别逻辑：
        # 理论上应该有，但是实际没有的 id，就是缺失的 episode_id
        missing_episode_ids = sorted(expected_episode_ids - actual_episode_ids)

    print("\nEpisode ID Continuity Check")
    print("--------------------------------")

    if len(missing_episode_ids) == 0:
        print("Episode IDs are continuous.")
    else:
        print("Missing episode IDs:")
        print(missing_episode_ids)

    print("\nEpisode ID Continuity Check Summary")
    print("--------------------------------")
    print(f"Unique episode_id count: {len(unique_episode_ids)}")
    print(f"Missing episode_id count: {len(missing_episode_ids)}")

    # =====================================================
    # Part 8: 检查 task 数据量是否均衡
    # =====================================================

    # 统计每个 task 有多少条 episode
    task_counts = df["task"].value_counts()

    print("\nTask Episode Count")
    print("--------------------------------")
    print(task_counts)

    if len(task_counts) == 0:
        min_task_count = 0
        max_task_count = 0
        task_imbalance_ratio = 0
        rare_tasks = task_counts
    else:
        min_task_count = task_counts.min()
        max_task_count = task_counts.max()

        if min_task_count == 0:
            task_imbalance_ratio = 0
        else:
            task_imbalance_ratio = max_task_count / min_task_count

        # 判别逻辑：
        # 找出样本数量少于 TASK_MIN_COUNT 的 task
        # 这些任务的数据太少，评测结果可能不稳定
        rare_tasks = task_counts[task_counts < TASK_MIN_COUNT]

    print("\nTask Balance Check")
    print("--------------------------------")

    if len(rare_tasks) == 0:
        print("No task has too few episodes.")
    else:
        print("Tasks with too few episodes:")
        print(rare_tasks)

    # 判别逻辑：
    # 如果最多任务数量 / 最少任务数量 超过阈值，说明任务数据分布不均衡
    if task_imbalance_ratio > TASK_IMBALANCE_RATIO:
        print("Task distribution is imbalanced.")
    else:
        print("Task distribution is acceptable.")

    print("\nTask Balance Check Summary")
    print("--------------------------------")
    print(f"Minimum task count: {min_task_count}")
    print(f"Maximum task count: {max_task_count}")
    print(f"Task imbalance ratio: {round(task_imbalance_ratio, 4)}")
    print(f"Task minimum count threshold: {TASK_MIN_COUNT}")
    print(f"Task imbalance ratio threshold: {TASK_IMBALANCE_RATIO}")

    report_lines = [
    "Robot Episode Data Quality Report v0.4",
    "================================================",
    "",
    "Required Column Check",
    "------------------------------------------------",
    ]

    if len(missing_columns) == 0:
        report_lines.append("All required columns exist.")
    else:
        report_lines.append("Missing required columns:")
        report_lines.append(str(missing_columns))

    report_lines.extend([
        "",
        "Missing Value Summary",
        "------------------------------------------------",
        missing_value_summary.to_string(),
        "",
        "Missing Value Check Summary",
        "------------------------------------------------",
        f"Total episode count: {total_episode_count}",
        f"Episodes with missing values: {missing_episode_count}",
        f"Missing episode rate: {round(missing_episode_rate, 4)}",
        "",
        "Success Label Check Summary",
        "------------------------------------------------",
        f"Invalid success label count: {invalid_success_count}",
        f"Invalid success label rate: {round(invalid_success_rate, 4)}",
        "",
        "Reward Check Summary",
        "------------------------------------------------",
        f"Reward valid range: [{REWARD_MIN}, {REWARD_MAX}]",
        f"Invalid reward count: {invalid_reward_count}",
        f"Invalid reward rate: {round(invalid_reward_rate, 4)}",
        "",
        "Steps Check Summary",
        "------------------------------------------------",
        f"Steps valid range: [{STEPS_MIN}, {STEPS_MAX}]",
        f"Invalid steps count: {invalid_steps_count}",
        f"Invalid steps rate: {round(invalid_steps_rate, 4)}",
        "",
        "Episode ID Duplicate Check Summary",
        "------------------------------------------------",
        f"Duplicated episode_id row count: {duplicated_episode_id_count}",
        "",
        "Episode ID Continuity Check Summary",
        "------------------------------------------------",
        f"Unique episode_id count: {len(unique_episode_ids)}",
        f"Missing episode_id count: {len(missing_episode_ids)}",
        "",
        "Task Episode Count",
        "------------------------------------------------",
        task_counts.to_string(),
        "",
        "Task Balance Check Summary",
        "------------------------------------------------",
        f"Minimum task count: {min_task_count}",
        f"Maximum task count: {max_task_count}",
        f"Task imbalance ratio: {round(task_imbalance_ratio, 4)}",
        f"Task minimum count threshold: {TASK_MIN_COUNT}",
        f"Task imbalance ratio threshold: {TASK_IMBALANCE_RATIO}",
    ])

    report_text = "\n".join(report_lines)

    RESULTS_DIR.mkdir(exist_ok=True)
    REPORT_PATH.write_text(report_text, encoding="utf-8")

    print(f"\nData quality report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()