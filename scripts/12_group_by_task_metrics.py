import sqlite3
from pathlib import Path

# 1. 找到数据库文件
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)

# 3. 创建 cursor
cursor = conn.cursor()

# 4. 按 task 分组计算指标
cursor.execute("""
SELECT
    task,
    COUNT(*) AS episode_count,
    AVG(success) AS success_rate,
    AVG(reward) AS average_reward,
    AVG(steps) AS average_steps
FROM episodes
GROUP BY task
""")

# 5. 取出所有分组结果
rows = cursor.fetchall()

# 6. 打印结果
print("按 task 分组的机器人 episode 指标：")

if len(rows) == 0:
    print("当前数据库中没有 episode 数据")
else:
    for row in rows:
        task = row[0]
        episode_count = row[1]
        success_rate = row[2]
        average_reward = row[3]
        average_steps = row[4]

        print("--------------------")
        print(f"task: {task}")
        print(f"episode_count: {episode_count}")
        print(f"success_rate: {success_rate:.2%}")
        print(f"average_reward: {average_reward:.2f}")
        print(f"average_steps: {average_steps:.2f}")

# 7. 关闭数据库连接
conn.close()