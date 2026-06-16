import csv
import sqlite3
from pathlib import Path

# 1. 文件路径
csv_path = Path("data") / "episodes_sql_demo.csv"
db_path = Path("data") / "robot_episodes.db"

# 2. 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. 读取 CSV，并转换成适合插入数据库的数据
episodes = []

with open(csv_path,"r",encoding="utf-8")as f :
    reader = csv.DictReader(f)

    for row in reader:
        episode = (
            int(row["episode_id"]),
            row["task"],
            float(row["reward"]),
            int(row["success"]),
            int(row["steps"]),
            row["failure_reason"]
        )

        episodes.append(episode)

# 4. 为了避免 episode_id 重复，先清空旧数据
cursor.execute("""
DELETE FROM episodes
""")

# 5. 批量插入 CSV 数据
cursor.executemany("""
INSERT INTO episodes (
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
)
VALUES (?, ?, ?, ?, ?, ?)
""", episodes)

# 6. 提交修改并关闭数据库
conn.commit()
conn.close()

print(f"成功从 {csv_path} 导入 {len(episodes)} 条 episode 数据到 SQLite")