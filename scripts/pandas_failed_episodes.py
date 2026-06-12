import pandas as pd
from pathlib import Path

DATA_PATH = Path("data") / "episodes.csv"


def main():

    df = pd.read_csv(DATA_PATH)

    print (df.head())
    
    total_episode_count = df.shape[0]

    failed_episodes = df[df["success"] == 0]
    failed_count = failed_episodes.shape[0]

    failed_rate = failed_count / total_episode_count

    print("\nFailed Episodes")
    print("--------------------------------")
    print(failed_episodes)

    print("\nFailure Summary")
    print("--------------------------------")
    print(f"Total episode count: {total_episode_count}")
    print(f"Failed episode count: {failed_count}")
    print(f"Failed rate: {round(failed_rate, 4)}")

    failed_task_counts = failed_episodes["task"].value_counts()
    print("\nFailed Episode Count by Task")
    print("--------------------------------")
    print(failed_task_counts)


if __name__ == "__main__":
    main()

