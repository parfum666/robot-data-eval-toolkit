import pymysql


# 1. 连接 MySQL 数据库
# 注意：下面这些参数需要根据你自己电脑上的 MySQL 配置修改
conn = pymysql.connect(
    host="localhost",        # MySQL 服务地址，本机一般是 localhost
    port=3306,               # MySQL 默认端口
    user="root",             # MySQL 用户名
    password="your_password",# MySQL 密码，需要替换成自己的
    database="robot_data_platform",
    charset="utf8mb4"
)

# 2. 创建 cursor，用来执行 SQL
cursor = conn.cursor()


# 3. 创建 episodes 表
cursor.execute("""
CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT PRIMARY KEY,
    task VARCHAR(100),
    reward DOUBLE,
    success INT,
    steps INT,
    failure_reason VARCHAR(255)
)
""")


# 4. 准备几条机器人 episode 数据
episodes = [
    (1, "pick_cube", 8.5, 1, 42, ""),
    (2, "pick_cube", 3.2, 0, 60, "grasp_failed"),
    (3, "open_drawer", 7.1, 1, 55, ""),
    (4, "open_drawer", 2.4, 0, 80, "timeout"),
    (5, "push_button", 9.0, 1, 35, "")
]


# 5. 批量插入 episode 数据
cursor.executemany("""
INSERT INTO episodes (
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
)
VALUES (%s, %s, %s, %s, %s, %s)
""", episodes)


# 6. 查询失败 episode，也就是 badcase
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
""")

badcases = cursor.fetchall()


# 7. 打印 badcase 查询结果
print("MySQL badcase episodes:")

for row in badcases:
    print(row)


# 8. 提交修改并关闭连接
conn.commit()
cursor.close()
conn.close()