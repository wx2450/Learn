import rclpy
from rclpy.node import Node


class MinimalNode(Node):
    """一个用于学习节点生命周期、参数、定时器和日志的最小 ROS 2 节点。"""

    def __init__(self) -> None:
        super().__init__('minimal_node')

        self.declare_parameter('message', 'Hello from pj1_basics')
        self.declare_parameter('period_sec', 1.0)

        self._message = self.get_parameter('message').value
        period_sec = self.get_parameter('period_sec').value
        if period_sec <= 0.0:
            self.get_logger().warning(
                "Parameter 'period_sec' must be positive; using 1.0 second."
            )
            period_sec = 1.0

        self._count = 0
        self._timer = self.create_timer(period_sec, self._on_timer)
        self.get_logger().info(
            f'Started with message={self._message!r}, period_sec={period_sec}.'
        )

    def _on_timer(self) -> None:
        self._count += 1
        self.get_logger().info(f'[{self._count}] {self._message}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MinimalNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
