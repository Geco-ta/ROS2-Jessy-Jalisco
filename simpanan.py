#node
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import threading

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')

        # Parameter port (bisa di-override lewat launch)
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 9600)
        port     = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value

        # Publisher: kirim data sensor ke topic
        self.sensor_pub = self.create_publisher(String, '/sensor_data', 10)

        # Subscriber: terima perintah servo dari topic
        self.create_subscription(String, '/servo_cmd', self.cmd_callback, 10)

        # Buka koneksi serial
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f'Serial terhubung di {port}')
        except serial.SerialException as e:
            self.get_logger().error(f'Gagal buka serial: {e}')
            raise

        # Thread baca serial
        self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.read_thread.start()

    def cmd_callback(self, msg):
        """Terima perintah dari keyboard node, kirim ke Arduino."""
        cmd = msg.data.upper() + '\n'
        self.ser.write(cmd.encode())
        self.get_logger().info(f'Kirim ke Arduino: {cmd.strip()}')

    def read_serial(self):
        """Baca data sensor dari Arduino, publish ke topic."""
        while rclpy.ok():
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith('SENSOR:'):
                    msg = String()
                    msg.data = line
                    self.sensor_pub.publish(msg)
                    self.get_logger().debug(f'Sensor: {line}')
            except Exception as e:
                self.get_logger().warn(f'Error baca serial: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='servo_controller',
            executable='serial_node',
            name='serial_node',
            parameters=[{'port': '/dev/ttyACM0'}],
            output='screen'
        ),
        Node(
            package='servo_controller',
            executable='teleop_key',
            name='teleop_key',
            output='screen',
            prefix='xterm -e'  # buka terminal baru untuk keyboard
        ),
    ])