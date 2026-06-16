import sqlite3
from pathlib import Path

# 1. 找到数据库文件
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)

# 3. 创建 cursor
cursor = conn.cursor()

# 4. 查询失败 episode，并按照 steps 从大到小排序
cursor.execute("""
SELECT
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
FROM episodes
WHERE success = 0
ORDER BY steps DESC
""")

# 5. 取出所有 badcase
rows = cursor.fetchall()

# 6. 打印结果
print("机器人 badcase 数据：")

if len(rows) == 0:
    print("当前没有失败 episode")
else:
    for row in rows:
        episode_id = row[0]
        task = row[1]
        reward = row[2]
        success = row[3]
        steps = row[4]
        failure_reason = row[5]

        print("--------------------")
        print(f"episode_id: {episode_id}")
        print(f"task: {task}")
        print(f"reward: {reward}")
        print(f"success: {success}")
        print(f"steps: {steps}")
        print(f"failure_reason: {failure_reason}")

# 7. 关闭数据库连接
conn.close()