import csv
from pathlib import Path

csv_path = Path("data")/ "episodes.csv"
report_path = Path("results") / "csv_eval_report_v02.txt"


total_reward =0
episode_count =0
success_count =0
total_steps = 0


with open(csv_path,"r",encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reward = float(row["reward"])
        success = float(row["success"])
        steps = int(row["steps"])

        total_reward = total_reward + reward
        episode_count = episode_count + 1
        if success ==1:
            success_count +=1
        total_steps = total_steps + steps

average_reward = total_reward / episode_count
success_rate = success_count / episode_count
average_steps = total_steps / episode_count

print("episode count:", episode_count)
print("total reward:", total_reward)
print("average reward:", average_reward)
print("success count:", success_count)
print("success rate:", success_rate)
print("average steps:", average_steps)

with open(report_path, "w", encoding="utf-8") as f:
    f.write("Robot Episode Evaluation Report\n")
    f.write("===============================\n")
    f.write(f"episode count: {episode_count}\n")
    f.write(f"total reward: {total_reward}\n")
    f.write(f"average reward: {average_reward}\n")
    f.write(f"success count: {success_count}\n")
    f.write(f"success rate: {success_rate}\n")
    f.write(f"average steps: {average_steps}\n")

print("report saved to:", report_path)