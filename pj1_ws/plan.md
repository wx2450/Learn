# pj1_ws ROS 2 入门项目计划

## 项目目标

在 `pj1_ws` 中完成一个不依赖 MuJoCo 的虚拟双关节机械臂控制项目，系统学习 ROS 2 的 Workspace、Package、Node、Topic、Service、Action、Parameter、Launch 和 YAML。

完成后，再将虚拟机械臂节点逐步替换为 MuJoCo 接口。

## 已确认环境

| 项目 | 当前状态 |
| --- | --- |
| ROS 2 | Jazzy |
| colcon | 可用，版本 0.21.0 |
| Python | `pj1_ws/.venv/bin/python`，Python 3.12.3 |
| ROS 2 Python 接口 | `rclpy` 可导入 |
| YAML | PyYAML 6.0.3，已安装到项目 `.venv` |

## 项目范围

- 第一阶段只实现纯 ROS 2 虚拟双关节系统。
- 不接入 MuJoCo、ros2_control、MoveIt 2、复杂视觉、强化学习、SLAM、Nav2 或真实硬件。
- 每次只推进一个步骤；仅在实际运行并验证后标记完成。

## 学习步骤

### 1. 最小 ROS 2 工作空间与 Python 包

- [x] 确认工作空间结构。
- [x] 创建第一个 ROS 2 Python Package。
- [x] 构建并运行最小节点。

完成标准：能够在当前工作空间中使用实际验证过的命令构建并运行一个 ROS 2 Python 节点。

### 2. Topic、Publisher、Subscriber 与 Timer

- [x] 创建发布者节点。
- [x] 创建订阅者节点。
- [x] 使用 Timer 周期发布消息。
- [x] 使用日志观察通信结果。

完成标准：两个节点运行时，订阅者能持续接收并输出发布者消息。

### 3. 虚拟双关节状态闭环

- [x] 创建虚拟机械臂节点。
- [x] 接收两关节目标角度。
- [x] 发布标准 `/joint_states`。
- [x] 创建监控节点并输出目标与实际角度误差。
- [x] 使用 Parameter 配置初始角度、更新频率和最大速度。

完成标准：发送目标角度后，虚拟关节状态逐步收敛，监控节点能显示误差变化。

### 4. Service

- [ ] 提供关节状态重置 Service。
- [ ] 验证请求、响应和重置后的状态发布。

完成标准：调用 Service 后，关节目标与当前状态均回到配置的初始值。

### 5. Action

- [ ] 定义关节目标执行 Action。
- [ ] 实现 Action Server。
- [ ] 实现 Action Client。
- [ ] 提供进度反馈、最终结果与取消处理。

完成标准：客户端可发送关节目标、接收执行反馈和结果，并能取消未完成任务。

### 6. Launch 与 YAML

- [ ] 用 YAML 管理节点参数。
- [ ] 创建 Launch 文件启动全部节点。
- [ ] 验证配置变更能生效。

完成标准：通过一个已验证的 Launch 命令启动系统，且参数来自 YAML 文件。

### 7. 系统验收与整理

- [ ] 检查节点、Topic、Service、Action 和参数。
- [ ] 完成一次 ROS 2 常见问题排查练习。
- [ ] 整理实际可用的构建、运行和验证命令。
- [ ] 更新项目说明与进度记录。

完成标准：系统可重复启动和验证，项目资料能反映实际目录、接口、命令和学习进度。

## 当前步骤

下一步：执行“Service”。
