import numpy as np
from pathlib import Path

# ------------------------------
# 1. 模拟机器人episode数据
# ------------------------------
episodes = [
    {"episode_id": 1, "reward": 20, "success": 1, "length": 5},
    {"episode_id": 2, "reward": 40, "success": 0, "length": 4},
    {"episode_id": 3, "reward": 30, "success": 1, "length": 6},
]

# ------------------------------
# 2. Python统计成功次数
# ------------------------------
success_count = sum(ep["success"] for ep in episodes)
total_count = len(episodes)
success_rate = success_count / total_count * 100

# ------------------------------
# 3. NumPy统计reward
# ------------------------------
rewards = np.array([ep["reward"] for ep in episodes])
mean_reward = rewards.mean()
max_reward = rewards.max()
min_reward = rewards.min()
sum_reward = rewards.sum()

# ------------------------------
# 4. 遍历data文件夹统计文件
# ------------------------------
data_dir = Path("data")
csv_count = 0
json_count = 0
jpg_count = 0

for file in data_dir.iterdir():
    if file.suffix == ".csv":
        csv_count += 1
    elif file.suffix == ".json":
        json_count += 1
    elif file.suffix == ".jpg":
        jpg_count += 1

# ------------------------------
# 5. 写入result.txt
# ------------------------------
result = f"""
Robot Episode Stats:
Total Episodes: {total_count}
Success Count: {success_count}
Success Rate: {success_rate:.2f}%
Mean Reward: {mean_reward}
Max Reward: {max_reward}
Min Reward: {min_reward}
Sum Reward: {sum_reward}

Data Folder Stats:
CSV files: {csv_count}
JSON files: {json_count}
JPG files: {jpg_count}
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("综合统计完成，结果已保存到 result.txt")