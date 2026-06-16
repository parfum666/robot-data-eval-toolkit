import sqlite3
from pathlib import Path

# 1. 找到数据库文件
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)

# 3. 创建 cursor
cursor = conn.cursor()

# 4. 查询失败 episode
cursor.execute("""
SELECT *
FROM episodes
WHERE success = 0
""")

# 5. 取出所有查询结果
rows = cursor.fetchall()

# 6. 打印结果
print("失败 episode 数据：")

for row in rows:
    print(row)

# 7. 关闭数据库连接
conn.close()