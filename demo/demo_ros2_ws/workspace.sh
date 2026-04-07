cd
mkdir ros2_ws #create a new directory for the ROS2 workspace
cd ros2_ws/
mkdir src #create a new directory for the source code
ls #check the contents of the ros2_ws directory, it should contain the src directory
colcon build #build the ROS2 workspace using colcon
ls #check the contents of the ros2_ws directory, it should now contain a build directory and an install directory
sudo apt install ros-dev-tools #install the ROS development tools
cd install
source setup.bash #source the setup.bash file to set up the ROS2 environment
cd
gedit .bashrc #open the .bashrc file in a text editor
#add the following line to the end of the .bashrc file to source the ROS2