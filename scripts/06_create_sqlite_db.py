import sqlite3
from pathlib import Path

db_path = Path("data") / "robot_episodes.db"

conn =sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS episodes(
    episode_id INTEGER PRIMARY KEY,
    task TEXT,
    reward REAL,
    success INTEGER,
    steps INTEGER,
    failure_reason TEXT
    
               )       

""")

conn.commit()

conn.close()

print("SQLite 数据库创建完成")
print(f"数据库路径: {db_path}")
print("episodes 表创建完成")