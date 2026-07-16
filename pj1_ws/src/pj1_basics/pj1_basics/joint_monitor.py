import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointMonitor(Node):
    """周期输出两关节的目标、当前状态和控制误差。"""

    _JOINT_NAMES = ('joint_1', 'joint_2')

    def __init__(self) -> None:
        super().__init__('joint_monitor')
        self.declare_parameter('log_period_sec', 1.0)
        log_period_sec = self.get_parameter('log_period_sec').value
        if log_period_sec <= 0.0:
            self.get_logger().warning(
                "Parameter 'log_period_sec' must be positive; using 1.0 second."
            )
            log_period_sec = 1.0

        self._target_positions: dict[str, float] = {}
        self._actual_positions: dict[str, float] = {}
        self._command_subscription = self.create_subscription(
            JointState,
            '/pj1/joint_command',
            self._on_command,
            10,
        )
        self._state_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self._on_state,
            10,
        )
        self._timer = self.create_timer(log_period_sec, self._log_error)
        self.get_logger().info(
            'Monitoring /pj1/joint_command and /joint_states.'
        )

    def _on_command(self, message: JointState) -> None:
        received_positions = dict(zip(message.name, message.position))
        self._target_positions = {
            joint_name: float(received_positions[joint_name])
            for joint_name in self._JOINT_NAMES
            if joint_name in received_positions
        }

    def _on_state(self, message: JointState) -> None:
        received_positions = dict(zip(message.name, message.position))
        self._actual_positions = {
            joint_name: float(received_positions[joint_name])
            for joint_name in self._JOINT_NAMES
            if joint_name in received_positions
        }

    def _log_error(self) -> None:
        if not self._target_positions or not self._actual_positions:
            self.get_logger().info('Waiting for a command and joint state.')
            return

        details = []
        for joint_name in self._JOINT_NAMES:
            if (
                joint_name not in self._target_positions
                or joint_name not in self._actual_positions
            ):
                continue
            target = self._target_positions[joint_name]
            actual = self._actual_positions[joint_name]
            details.append(
                f'{joint_name}: target={target:.3f}, actual={actual:.3f}, '
                f'error={target - actual:.3f}'
            )

        if details:
            self.get_logger().info(' | '.join(details))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = JointMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
