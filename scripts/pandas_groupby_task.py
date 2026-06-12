from pathlib import Path

import pandas as pd

DATA_PATH = Path("data") / "episodes.csv"


def main():
  
    df = pd.read_csv(DATA_PATH)

  
    print("First 5 rows:")
    print(df.head())

  
    total_episode_count = df.shape[0]
    overall_average_reward = df["reward"].mean()
    overall_success_rate = df["success"].mean()
    overall_average_steps = df["steps"].mean()

    print("\nOverall Evaluation")
    print("--------------------------------")
    print(f"Total episode count: {total_episode_count}")
    print(f"Overall average reward: {round(overall_average_reward, 4)}")
    print(f"Overall success rate: {round(overall_success_rate, 4)}")
    print(f"Overall average steps: {round(overall_average_steps, 4)}")

    grouped_by_task = df.groupby("task")

    task_episode_count = grouped_by_task["episode_id"].count()
    task_average_reward = grouped_by_task["reward"].mean()
    task_success_rate = grouped_by_task["success"].mean()
    task_average_steps = grouped_by_task["steps"].mean()

    print("\nTask-level Average Reward")
    print("--------------------------------")
    print(task_average_reward)

    print("\nTask-level Success Rate")
    print("--------------------------------")
    print(task_success_rate)

    print("\nTask-level Average Steps")
    print("--------------------------------")
    print(task_average_steps)

    task_report = grouped_by_task.agg(
        episode_count = ("episode_id","count"),
        reward_average = ("reward","mean"),
        success_rate=("success", "mean"),
        average_steps=("steps", "mean"),
    )

    task_report = task_report.round(4)

    print("\nTask-level Evaluation Report")
    print("--------------------------------")
    print(task_report)

    


if __name__ == "__main__":
        main()


  