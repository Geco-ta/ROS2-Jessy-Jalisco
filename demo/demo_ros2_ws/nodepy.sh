cd ros2_ws/src/my_py_pkg/my_py_pkg #navigate to the my_py_pkg directory
touch my_first_node.py #create a new Python file for the ROS2 node
# go to the my_first_node.py file and add the following code to create a simple ROS2 node that prints "Hello, ROS2!" to the console every second
### add the following code to the my_first_node.py file
{
    #! /usr/bin/env python3
    import rclpy
    from rclpy.node import Node

    def main(args=None):
        rclpy.init(args=args)
        node = Node('my_first_node')
        node.get_logger().info('Hello, ROS2!')
        rclpy.spin(node)
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
}
#save the my_first_node.py file and make it executable
chmod +x my_first_node.py
#navigate back to the ros2_ws directory and build the ROS2 workspace using colcon
cd ../../.. #navigate back to the ros2_ws directory
colcon build --packages-select my_py_pkg #build only the my_py_pkg package
#source the setup.bash file to set up the ROS2 environment
source install/setup.bash
#run the my_first_node.py node using ros2 run
ros2 run my_py_pkg my_first_node.py
#you should see "Hello, ROS2!" printed to the console every second
#ctrl + c to stop the my_first_node.py node