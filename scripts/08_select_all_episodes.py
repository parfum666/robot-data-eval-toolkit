import sqlite3
from pathlib import Path


db_path = Path("data") / "robot_episodes.db"

conn = sqlite3.connect(db_path)


cursor = conn.cursor()


cursor.execute(
"""
SELECT *
FROM episodes
"""
)

rows = cursor.fetchall()
print("episodes 表中的所有数据：")

for row in rows:
    print(row)


conn.close()