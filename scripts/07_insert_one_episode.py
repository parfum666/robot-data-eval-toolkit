import sqlite3
from pathlib import Path

db_path = Path("data") /  "robot_episodes.db"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

episodes = [
(3,"Lift",8.5,1,120,"") ,
(4, "Lift", 1.5, 0, 220, "timeout"),

]

cursor.executemany("""
INSERT INTO episodes(
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
            )
VALUES(?,?,?,?,?,?)
""",episodes)
               
               
               
               
conn.commit()
conn.close()
