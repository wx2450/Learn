import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MessagePublisher(Node):
    """周期发布 String 消息，用于学习 ROS 2 Topic 与 Timer。"""

    def __init__(self) -> None:
        super().__init__('message_publisher')

        self.declare_parameter('message', 'Hello from message_publisher')
        self.declare_parameter('period_sec', 1.0)

        self._message = self.get_parameter('message').value
        period_sec = self.get_parameter('period_sec').value
        if period_sec <= 0.0:
            self.get_logger().warning(
                "Parameter 'period_sec' must be positive; using 1.0 second."
            )
            period_sec = 1.0

        self._publisher = self.create_publisher(String, '/pj1/chatter', 10)
        self._count = 0
        self._timer = self.create_timer(period_sec, self._publish_message)
        self.get_logger().info(
            f'Publishing to /pj1/chatter every {period_sec} second(s).'
        )

    def _publish_message(self) -> None:
        self._count += 1
        message = String()
        message.data = f'[{self._count}] {self._message}'
        self._publisher.publish(message)
        self.get_logger().info(f'Published: {message.data}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MessagePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
