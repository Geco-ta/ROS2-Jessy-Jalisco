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
            prefix='xterm -e'
        ),
        # Tambah RViz2
       
    ])