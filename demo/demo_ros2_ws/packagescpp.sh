cd ros2_ws/src/ #navigate to the src directory of the ROS2 workspace
ros2 pkg create my_cpp_pkg --build-type ament_cmake --dependencies rclcpp # create a new ROS2 package named my_cpp_pkg with ament_cmake build type and rclcpp dependency
colcon build #build the ROS2 workspace using colcon
rm -r build/ install/ log/ #remove the build, install, and log directories to clean up the workspace
cd .. #navigate back to the ros2_ws directory
colcon build --packages-select my_cpp_pkg #build only the my_cpp_pkg package
