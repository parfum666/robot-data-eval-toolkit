USE robot_data_platform;

-- 1. 插入机器人 episode 数据
INSERT INTO episodes (
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
)
VALUES
(1, 'pick_cube', 8.5, 1, 42, ''),
(2, 'pick_cube', 3.2, 0, 60, 'grasp_failed'),
(3, 'open_drawer', 7.1, 1, 55, ''),
(4, 'open_drawer', 2.4, 0, 80, 'timeout'),
(5, 'push_button', 9.0, 1, 35, '');

-- 2. 查询所有 episode
SELECT
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
FROM episodes;

-- 3. 查询失败 episode，也就是 badcase
SELECT
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
FROM episodes
WHERE success = 0;

-- 4. 按 task 查询 episode
SELECT
    episode_id,
    task,
    reward,
    success,
    steps,
    failure_reason
FROM episodes
WHERE task = 'pick_cube';

-- 5. 计算整体指标
SELECT
    COUNT(*) AS episode_count,
    AVG(success) AS success_rate,
    AVG(reward) AS average_reward,
    AVG(steps) AS average_steps
FROM episodes;

-- 6. 按 task 分组统计指标
SELECT
    task,
    COUNT(*) AS episode_count,
    AVG(success) AS success_rate,
    AVG(reward) AS average_reward,
    AVG(steps) AS average_steps
FROM episodes
GROUP BY task;