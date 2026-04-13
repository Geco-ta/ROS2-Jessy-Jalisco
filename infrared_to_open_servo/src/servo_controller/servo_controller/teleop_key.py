import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
import tty
import termios

HELP = """
=== Servo Keyboard Controller ===
  O : Buka servo
  C : Tutup servo
  A : Mode AUTO (sensor kontrol)
  Q : Keluar
=================================
"""

class TeleopKey(Node):
    def __init__(self):
        super().__init__('teleop_key')
        self.pub = self.create_publisher(String, '/servo_cmd', 10)
        print(HELP)

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    def run(self):
        while rclpy.ok():
            key = self.get_key().lower()
            msg = String()

            if key == 'o':
                msg.data = 'OPEN'
                self.get_logger().info('Servo: BUKA')
            elif key == 'c':
                msg.data = 'CLOSE'
                self.get_logger().info('Servo: TUTUP')
            elif key == 'a':
                msg.data = 'AUTO'
                self.get_logger().info('Mode: AUTO (sensor)')
            elif key == 'q':
                self.get_logger().info('Keluar...')
                break
            else:
                continue

            self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TeleopKey()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()