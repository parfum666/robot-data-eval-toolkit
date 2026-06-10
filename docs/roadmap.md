# Roadmap

本项目是一个长期求职项目，用来逐步展示机器人数据闭环与评测方向的学习过程。

## v0.1 Basic Analyzer

Status: Finished

- 手动构造 episode 数据
- 统计 success rate
- 使用 NumPy 统计 reward
- 遍历 data 文件夹
- 写入 result.txt

## v0.2 CSV Reader

Next step:

- 学习读取 CSV 文件
- 从 episode_log.csv 中自动获取 episode 数据
- 替代当前手动构造的 episodes

## v0.3 Data Quality Checker

Planned:

- 检查空文件
- 检查缺失字段
- 检查异常 reward
- 检查 success 是否只包含 0/1

## v0.4 Visualization

Planned:

- reward 曲线
- success rate 可视化
- episode_length 分布

## v0.5 Evaluation Toolkit

Planned:

- 更完整的评测报告
- 更清晰的项目代码结构
- 支持更多数据格式
