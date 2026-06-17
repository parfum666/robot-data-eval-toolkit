"""
任务目标：
用 Python 列表模拟 MongoDB collection，
并完成机器人 episode 文档的基础查询。

这个 demo 用于理解：
1. MongoDB 的 collection 类似一组 document；
2. document 可以用 Python dict 表示；
3. collection 可以用 Python list 表示；
4. 可以按 task 查询 episode；
5. 可以查询 success = 0 的 badcase；
6. 可以访问 metadata、files 等嵌套字段。
"""

# 1. 用 list[dict] 模拟 MongoDB 中的 episodes collection
episodes_collection = [
    {
        "episode_id": 1,
        "task": "pick_cube",
        "reward": 8.5,
        "success": 1,
        "steps": 42,
        "failure_reason": "",
        "metadata": {
            "robot": "Panda",
            "simulator": "robosuite",
            "camera": "frontview"
        },
        "files": {
            "trajectory": "data/trajectories/episode_1.mcap",
            "log": "data/logs/episode_1.json"
        }
    },
    {
        "episode_id": 2,
        "task": "pick_cube",
        "reward": 3.2,
        "success": 0,
        "steps": 60,
        "failure_reason": "grasp_failed",
        "metadata": {
            "robot": "Panda",
            "simulator": "robosuite",
            "camera": "frontview"
        },
        "files": {
            "trajectory": "data/trajectories/episode_2.mcap",
            "log": "data/logs/episode_2.json"
        }
    },
    {
        "episode_id": 3,
        "task": "open_drawer",
        "reward": 7.1,
        "success": 1,
        "steps": 55,
        "failure_reason": "",
        "metadata": {
            "robot": "Panda",
            "simulator": "robosuite",
            "camera": "sideview"
        },
        "files": {
            "trajectory": "data/trajectories/episode_3.mcap",
            "log": "data/logs/episode_3.json"
        }
    },
    {
        "episode_id": 4,
        "task": "open_drawer",
        "reward": 2.4,
        "success": 0,
        "steps": 80,
        "failure_reason": "timeout",
        "metadata": {
            "robot": "Panda",
            "simulator": "robosuite",
            "camera": "sideview"
        },
        "files": {
            "trajectory": "data/trajectories/episode_4.mcap",
            "log": "data/logs/episode_4.json"
        }
    },
    {
        "episode_id": 5,
        "task": "lift_cube",
        "reward": 2.9,
        "success": 0,
        "steps": 90,
        "failure_reason": "object_dropped",
        "metadata": {
            "robot": "Panda",
            "simulator": "robosuite",
            "camera": "frontview"
        },
        "files": {
            "trajectory": "data/trajectories/episode_5.mcap",
            "log": "data/logs/episode_5.json"
        }
    }
]


# 2. 查询所有 episode
print("All Episodes")
print("-----------------------------------")

for episode in episodes_collection:
    print(
        episode["episode_id"],
        episode["task"],
        episode["reward"],
        episode["success"],
        episode["steps"]
    )


# 3. 按 task 查询 episode
target_task = "pick_cube"

print("\nEpisodes with task =", target_task)
print("-----------------------------------")

for episode in episodes_collection:
    if episode["task"] == target_task:
        print(
            episode["episode_id"],
            episode["task"],
            episode["reward"],
            episode["success"],
            episode["steps"]
        )


# 4. 查询失败 episode，也就是 badcase
print("\nBadcase Episodes")
print("-----------------------------------")

for episode in episodes_collection:
    if episode["success"] == 0:
        print(
            episode["episode_id"],
            episode["task"],
            episode["failure_reason"],
            episode["steps"]
        )


# 5. 查询使用 frontview camera 的 episode
target_camera = "frontview"

print("\nEpisodes with camera =", target_camera)
print("-----------------------------------")

for episode in episodes_collection:
    if episode["metadata"]["camera"] == target_camera:
        print(
            episode["episode_id"],
            episode["task"],
            episode["metadata"]["camera"],
            episode["files"]["trajectory"]
        )