from pathlib import Path
import pandas as pd

DATA_PATH = Path("data") / "episodes.csv"

def main():

    df=pd.read_csv(DATA_PATH)


    print("First 5 rows:")
    print(df.head())

    episode_count = df.shape[0]

    average_reward = df["reward"].mean()
    

    success_rate = df["success"].mean()

    average_steps = df["steps"].mean()

    print("\nPandas Basic Evaluation Report")
    print("--------------------------------")
    print(f"Episode count: {episode_count}")
    print(f"Average reward: {round(average_reward, 4)}")
    print(f"Success rate: {round(success_rate, 4)}")
    print(f"Average steps: {round(average_steps, 4)}")



if __name__ == "__main__":
    main()