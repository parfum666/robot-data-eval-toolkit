import sqlite3
from pathlib import Path

# 1. 找到数据库文件
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)

# 3. 创建 cursor
cursor = conn.cursor()

# 4. 指定要查询的任务名
task_name = "Lift"

# 5. 按 task 查询 episode
cursor.execute("""
SELECT *
FROM episodes
WHERE task = ?
""", (task_name,))

# 6. 取出查询结果
rows = cursor.fetchall()

# 7. 打印结果
print(f"{task_name} 任务的 episode 数据：")

for row in rows:
    print(row)

# 8. 关闭数据库连接
conn.close()