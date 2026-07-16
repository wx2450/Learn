import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class VirtualArm(Node):
    """用匀速响应模拟两关节机械臂的状态变化。"""

    _JOINT_NAMES = ('joint_1', 'joint_2')

    def __init__(self) -> None:
        super().__init__('virtual_arm')

        self.declare_parameter('initial_joint_positions', [0.0, 0.0])
        self.declare_parameter('update_rate_hz', 20.0)
        self.declare_parameter('max_velocity_rad_s', 1.0)

        initial_positions = list(
            self.get_parameter('initial_joint_positions').value
        )
        if len(initial_positions) != len(self._JOINT_NAMES):
            self.get_logger().warning(
                "Parameter 'initial_joint_positions' must contain two values; "
                'using [0.0, 0.0].'
            )
            initial_positions = [0.0, 0.0]

        update_rate_hz = self.get_parameter('update_rate_hz').value
        if update_rate_hz <= 0.0:
            self.get_logger().warning(
                "Parameter 'update_rate_hz' must be positive; using 20.0 Hz."
            )
            update_rate_hz = 20.0

        self._max_velocity = self.get_parameter('max_velocity_rad_s').value
        if self._max_velocity <= 0.0:
            self.get_logger().warning(
                "Parameter 'max_velocity_rad_s' must be positive; using 1.0 rad/s."
            )
            self._max_velocity = 1.0

        self._period_sec = 1.0 / update_rate_hz
        self._positions = [float(position) for position in initial_positions]
        self._target_positions = list(self._positions)

        self._state_publisher = self.create_publisher(JointState, '/joint_states', 10)
        self._command_subscription = self.create_subscription(
            JointState,
            '/pj1/joint_command',
            self._on_joint_command,
            10,
        )
        self._timer = self.create_timer(self._period_sec, self._update_state)
        self.get_logger().info(
            'Virtual arm started: publishing /joint_states and listening on '
            '/pj1/joint_command.'
        )

    def _on_joint_command(self, message: JointState) -> None:
        command_positions = dict(zip(message.name, message.position))
        missing_joints = [
            joint_name
            for joint_name in self._JOINT_NAMES
            if joint_name not in command_positions
        ]
        if missing_joints:
            self.get_logger().warning(
                'Ignoring command; missing position for: '
                f'{", ".join(missing_joints)}.'
            )
            return

        self._target_positions = [
            float(command_positions[joint_name]) for joint_name in self._JOINT_NAMES
        ]
        self.get_logger().info(
            f'New target: {dict(zip(self._JOINT_NAMES, self._target_positions))}'
        )

    def _update_state(self) -> None:
        maximum_step = self._max_velocity * self._period_sec
        velocities = []

        for index, target in enumerate(self._target_positions):
            error = target - self._positions[index]
            step = math.copysign(min(abs(error), maximum_step), error)
            self._positions[index] += step
            velocities.append(step / self._period_sec)

        state = JointState()
        state.header.stamp = self.get_clock().now().to_msg()
        state.name = list(self._JOINT_NAMES)
        state.position = self._positions
        state.velocity = velocities
        self._state_publisher.publish(state)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = VirtualArm()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
