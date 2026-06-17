CREAT DATABASE IF NOT EXISTS robot_data_platform;

USE robot_data_platform;

CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT PRIMARY KEY,
    task VARCHAR(100),
    reward DOUBLE,
    success INT,
    steps INT,
    failure_reason VARCHAR(255)
);

