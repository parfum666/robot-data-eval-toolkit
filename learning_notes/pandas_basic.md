# Pandas Basic Notes

## v0.3 Pandas Episode Evaluation

In v0.3, I learned how to use Pandas to analyze robot episode evaluation data.

The input file is:

```text
data/episodes.csv
```

Each row represents one robot episode. The main columns include:

```text
episode_id
task
reward
success
steps
```

## Key Pandas Operations

### 1. Read CSV

```python
df = pd.read_csv("data/episodes.csv")
```

This reads the CSV file into a Pandas DataFrame.

### 2. Preview Data

```python
df.head()
```

This shows the first five rows of the episode table.

### 3. Inspect DataFrame Structure

```python
df.shape
df.columns
```

`df.shape` shows the number of rows and columns.
`df.columns` shows all column names.

### 4. Select One Column

```python
df["reward"]
```

This selects the reward column from the DataFrame.

### 5. Calculate Basic Metrics

```python
df["reward"].mean()
df["success"].mean()
df["steps"].mean()
```

These are used to calculate average reward, success rate, and average steps.

### 6. Group by Task

```python
df.groupby("task").agg(
    episode_count=("episode_id", "count"),
    average_reward=("reward", "mean"),
    success_rate=("success", "mean"),
    average_steps=("steps", "mean"),
)
```

This generates task-level evaluation metrics.

### 7. Analyze Failed Episodes

```python
failed_episodes = df[df["success"] == 0]
failed_task_counts = failed_episodes["task"].value_counts()
```

This filters failed episodes and counts which tasks fail most often.

## Summary

Compared with csv.DictReader in v0.2, Pandas makes it easier to analyze robot episode data at the table level. It can quickly calculate overall metrics, task-level metrics, and failed episode statistics, which are useful for robot data evaluation and data loop analysis.
