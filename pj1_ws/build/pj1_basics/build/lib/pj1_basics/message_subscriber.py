import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MessageSubscriber(Node):
    """订阅 String 消息，用于观察 ROS 2 Topic 回调。"""

    def __init__(self) -> None:
        super().__init__('message_subscriber')
        self._subscription = self.create_subscription(
            String,
            '/pj1/chatter',
            self._on_message,
            10,
        )
        self.get_logger().info('Subscribed to /pj1/chatter.')

    def _on_message(self, message: String) -> None:
        self.get_logger().info(f'Received: {message.data}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MessageSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
