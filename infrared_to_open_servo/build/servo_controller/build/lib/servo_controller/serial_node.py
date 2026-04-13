import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState, Range
from visualization_msgs.msg import Marker
import serial
import threading
import math
from builtin_interfaces.msg import Time

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 9600)
        port     = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value

        # Publisher lama
        self.sensor_pub = self.create_publisher(String, '/sensor_data', 10)
        self.create_subscription(String, '/servo_cmd', self.cmd_callback, 10)

        # Publisher RViz2
        self.joint_pub  = self.create_publisher(JointState, '/joint_states', 10)
        self.range_pub  = self.create_publisher(Range, '/sensor_range', 10)
        self.marker_pub = self.create_publisher(Marker, '/servo_marker', 10)

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f'Serial terhubung di {port}')
        except serial.SerialException as e:
            self.get_logger().error(f'Gagal buka serial: {e}')
            raise

        self.servo_pos = 0
        self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.read_thread.start()

    def cmd_callback(self, msg):
        cmd = msg.data.upper() + '\n'
        self.ser.write(cmd.encode())

    def read_serial(self):
        while rclpy.ok():
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith('SENSOR:'):
                    # Parse: SENSOR:512,SERVO:180
                    parts = line.split(',')
                    sensor_val = int(parts[0].split(':')[1])
                    servo_val  = int(parts[1].split(':')[1])
                    self.servo_pos = servo_val

                    # Publish String (lama)
                    msg = String()
                    msg.data = line
                    self.sensor_pub.publish(msg)

                    # Publish ke RViz2
                    self.publish_joint(servo_val)
                    self.publish_range(sensor_val)
                    self.publish_marker(servo_val)

            except Exception as e:
                self.get_logger().warn(f'Error: {e}')

    def publish_joint(self, servo_deg):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name     = ['servo_joint']
        msg.position = [math.radians(servo_deg)]  # konversi ke radian
        self.joint_pub.publish(msg)

    def publish_range(self, sensor_val):
        msg = Range()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'sensor_frame'
        msg.radiation_type  = Range.INFRARED
        msg.field_of_view   = 0.1
        msg.min_range       = 0.0
        msg.max_range       = 1.0
        msg.range           = sensor_val / 1023.0  # normalisasi 0.0 - 1.0
        self.range_pub.publish(msg)

    def publish_marker(self, servo_deg):
        msg = Marker()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.type            = Marker.ARROW
        msg.action          = Marker.ADD
        msg.scale.x         = 0.1
        msg.scale.y         = 0.02
        msg.scale.z         = 0.02
        # Warna: hijau = buka, merah = tutup
        msg.color.a = 1.0
        msg.color.r = 0.0 if servo_deg > 90 else 1.0
        msg.color.g = 1.0 if servo_deg > 90 else 0.0
        msg.color.b = 0.0
        self.marker_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()