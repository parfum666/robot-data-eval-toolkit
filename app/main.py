import sqlite3
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(title="Robot Episode Data API")
db_path = Path("data") / "robot_episodes.db"

@app.get("/episodes")
def get_episodes():
    conn = sqlite3.connect(db_path)
    cursor =conn.cursor()

    cursor.execute("""
    SELECT
        episode_id,
        task,
        reward,
        success,
        steps,
        failure_reason
    FROM episodes
                   """)
    rows = cursor.fetchall()

    conn.close()

    episodes =[]

    for row in rows:
        episode = {
            "episode_id": row[0],
            "task": row[1],
            "reward": row[2],
            "success": row[3],
            "steps": row[4],
            "failure_reason": row[5]
        }
        episodes.append(episode)

    return {
        "episode_count": len(episodes),
        "data": episodes
    }
    
@app.get("/metrics")   
def get_metrics():
    conn = sqlite3.connect(db_path)
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

    conn.close()

    episode_count = result[0]
    success_rate = result[1]
    average_reward = result[2]
    average_steps = result[3]

    # 6. 返回 JSON
    return {
        "episode_count": episode_count,
        "success_rate": success_rate,
        "average_reward": average_reward,
        "average_steps": average_steps
    }

@app.get("/tasks")
def get_tasks():
    # 1. 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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
    
    rows = cursor.fetchall()
    conn.close()

    task_metrics = []

    for row in rows:
        task_info = {
            "task": row[0],
            "episode_count": row[1],
            "success_rate": row[2],
            "average_reward": row[3],
            "average_steps": row[4]
        }

        task_metrics.append(task_info)

    # 6. 返回给浏览器
    return {
        "task_count": len(task_metrics),
        "data": task_metrics
    }

@app.get("/badcases")
def get_badcases():
    # 1. 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. 查询失败 episode，并按 steps 从大到小排序
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

    # 3. 取出所有失败 episode
    rows = cursor.fetchall()

    # 4. 关闭数据库连接
    conn.close()

    # 5. 把数据库元组转换成 JSON 字典列表
    badcases = []

    for row in rows:
        badcase = {
            "episode_id": row[0],
            "task": row[1],
            "reward": row[2],
            "success": row[3],
            "steps": row[4],
            "failure_reason": row[5]
        }

        badcases.append(badcase)

    # 6. 返回给浏览器
    return {
        "badcase_count": len(badcases),
        "data": badcases
    }