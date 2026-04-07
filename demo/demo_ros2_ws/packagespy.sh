cd ros2_ws/src/ #navigate to the src directory of the ROS2 workspace
ls #check the contents of the src directory, it should be empty
ros2 pkg create my_py_pkg --build-type ament_python --dependencies rclpy
cd .. #navigate back to the ros2_ws directory
colcon build #build the ROS2 workspace using colcon
colcon build --packages-select my_py_pkg #build only the my_py_pkg package