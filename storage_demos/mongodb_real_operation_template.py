"""
任务目标：
演示真实 MongoDB 中如何存储和查询机器人 episode 文档。

这个 demo 对应岗位要求中的：
“熟悉 MySQL、MongoDB 等存储组件的使用”。

当前文件用于学习 MongoDB 的基础操作结构：
1. 使用 pymongo 连接 MongoDB；
2. 向 episodes collection 插入一条 episode 文档；
3. 查询 success = 0 的 badcase；
4. 按 task 查询 episode；
5. 查询嵌套字段 metadata.camera。

注意：
如果本机还没有安装 MongoDB 和 pymongo，当前阶段先不用运行。
"""

from pymongo import MongoClient


# 1. 连接本机 MongoDB 服务
# MongoDB 默认地址是 mongodb://localhost:27017/
client = MongoClient("mongodb://localhost:27017/")


# 2. 选择数据库
# 如果数据库不存在，MongoDB 会在真正写入数据时自动创建
db = client["robot_data_platform"]


# 3. 选择 collection
# collection 类似 MySQL 里的 table
episodes_collection = db["episodes"]


# 4. 准备一条机器人 episode 文档
episode_document = {
    "episode_id": 15,
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
        "trajectory": "data/trajectories/episode_15.mcap",
        "rgb_video": "data/videos/episode_15_frontview.mp4",
        "log": "data/logs/episode_15.json"
    }
}


# 5. 插入一条 episode 文档
insert_result = episodes_collection.insert_one(episode_document)

print("Inserted document id:", insert_result.inserted_id)


# 6. 查询一条 episode
one_episode = episodes_collection.find_one({"episode_id": 15})

print("\nFind one episode:")
print(one_episode)


# 7. 查询失败 episode，也就是 badcase
badcases = episodes_collection.find({"success": 0})

print("\nBadcase episodes:")
for episode in badcases:
    print(
        episode["episode_id"],
        episode["task"],
        episode["failure_reason"],
        episode["steps"]
    )


# 8. 按 task 查询
lift_cube_episodes = episodes_collection.find({"task": "lift_cube"})

print("\nEpisodes with task = lift_cube:")
for episode in lift_cube_episodes:
    print(
        episode["episode_id"],
        episode["task"],
        episode["reward"],
        episode["success"]
    )


# 9. 查询嵌套字段 metadata.camera
frontview_episodes = episodes_collection.find({"metadata.camera": "frontview"})

print("\nEpisodes with camera = frontview:")
for episode in frontview_episodes:
    print(
        episode["episode_id"],
        episode["task"],
        episode["metadata"]["camera"]
    )