"""
任务目标：
用 Python 字典模拟 MongoDB 中的一条机器人 episode 文档。

这个 demo 用于理解：
1. MongoDB 的 document 类似 JSON；
2. 一条机器人 episode 不仅可以保存基础字段；
3. 还可以保存 metadata、files、sensor_info 等嵌套信息；
4. MongoDB 更适合保存结构灵活的机器人 episode 元数据。
"""

# 1. 用 Python dict 表示一条 MongoDB 风格的 episode 文档
episode_document = {
    "episode_id": 15,
    "task": "lift_cube",
    "reward": 2.9,
    "success": 0,
    "steps": 90,
    "failure_reason": "object_dropped",

    # 2. metadata 用来保存机器人、仿真环境、控制器等元信息
    "metadata": {
        "robot": "Panda",
        "simulator": "robosuite",
        "controller": "OSC_POSE",
        "camera": "frontview"
    },

    # 3. files 用来保存和这个 episode 相关的数据文件路径
    "files": {
        "trajectory": "data/trajectories/episode_15.mcap",
        "rgb_video": "data/videos/episode_15_frontview.mp4",
        "log": "data/logs/episode_15.json"
    },

    # 4. sensor_info 用来保存传感器相关信息
    "sensor_info": {
        "has_rgb": True,
        "has_depth": False,
        "has_joint_state": True,
        "control_frequency": 20
    }
}

# 5. 打印基础 episode 信息
print("MongoDB-style Robot Episode Document")
print("-----------------------------------")
print("episode_id:", episode_document["episode_id"])
print("task:", episode_document["task"])
print("reward:", episode_document["reward"])
print("success:", episode_document["success"])
print("steps:", episode_document["steps"])
print("failure_reason:", episode_document["failure_reason"])

# 6. 打印嵌套的 metadata 信息
print("\nMetadata")
print("-----------------------------------")
print("robot:", episode_document["metadata"]["robot"])
print("simulator:", episode_document["metadata"]["simulator"])
print("controller:", episode_document["metadata"]["controller"])
print("camera:", episode_document["metadata"]["camera"])

# 7. 打印文件路径信息
print("\nRelated Files")
print("-----------------------------------")
print("trajectory:", episode_document["files"]["trajectory"])
print("rgb_video:", episode_document["files"]["rgb_video"])
print("log:", episode_document["files"]["log"])

# 8. 判断是否是 badcase
if episode_document["success"] == 0:
    print("\nThis episode is a badcase.")
else:
    print("\nThis episode is successful.")