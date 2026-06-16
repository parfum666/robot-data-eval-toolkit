import sqlite3
from pathlib import Path

# 1. 找到数据库文件
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)

# 3. 创建 cursor
cursor = conn.cursor()

cursor.execute("""
SELECT
    COUNT(*) AS episode_count,
    AVG(success) AS success_rate,
    AVG(reward) AS average_reward,
    AVG(steps) AS average_steps
FROM episodes
""")

result = cursor.fetchone()

episode_count = result[0]
success_rate = result[1]
average_reward = result[2]
average_steps = result[3]

# 6. 打印结果
print("机器人 episode 整体指标：")

if episode_count == 0:
    print("当前数据库中没有 episode 数据")
else:
    print(f"episode_count: {episode_count}")
    print(f"success_rate: {success_rate:.2%}")
    print(f"average_reward: {average_reward:.2f}")
    print(f"average_steps: {average_steps:.2f}")

# 7. 关闭数据库连接
conn.close()