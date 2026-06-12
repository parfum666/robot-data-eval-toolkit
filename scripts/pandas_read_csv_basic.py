import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")/"episodes.csv"

def main():

    df = pd.read_csv(DATA_PATH)

    print("CSV loaded successfully.")
    print("Data type:")
    print(type(df))

   
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nFirst 3 rows:")
    print(df.head(3))

    print("data frame shape:",df.shape)

    episodes_count = df.shape[0]
    column_count =df.shape[1]

    print("\nEpisode count:")
    print(episodes_count)

    print("\nColumn count:")
    print(column_count)

    print("\nColumn names:")
    print(df.columns)

    print("\nReward column:")
    print(df["reward"])

    print("\ntask column:")
    print(df["task"])



if __name__ == "__main__":
    main()