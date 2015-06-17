#!/usr/bin/env bash

reset_ws=${1:-true}
catkin_ws=${2:-"$HOME/catkin_ws"}
repositories_dirs=${3:-"crob_gazebo_models dynamic_robot_localization dynamic_robot_localization_tests guardian_ros_pkg laserscan_to_pointcloud pose_to_tf_publisher robot_localization_tools"}

cd "${catkin_ws}/src/"
if [ $? -ne 0 ]; then
	exit -1
fi


echo -e "\n\n"
echo "####################################################################################################"
echo "##### Updating git repositories"
if [ "${reset_ws}" = true ] ; then
	echo "##### git reset --hard HEAD will be performed before pulling"
fi
echo -e "####################################################################################################\n"


for git_repository in ${repositories_dirs}
do
	cd "${git_repository}" &> /dev/null
	if [ $? -eq 0 ]; then
		echo -e "\n\n-------------------------------------------"
		echo "==> Updating ${git_repository}"
		if [ "${reset_ws}" = true ] ; then
			git reset --hard HEAD
		fi
		git pull
		cd ..
	fi
done



echo -e "\n\n"
echo "----------------------------------------------------------------------------------------------------"
echo ">>>>> Update finished"
echo "----------------------------------------------------------------------------------------------------"



echo -e "\n\n"
echo "####################################################################################################"
echo "##### Building catkin workspace"
echo "####################################################################################################"

cd "${catkin_ws}"
find ./src -name "*.bash" -exec chmod +x {} \;
find ./src -name "*.cfg" -exec chmod +x {} \;
find ./src -name "*.sh" -exec chmod +x {} \;


catkin_make

echo -e "\n\n"
echo "----------------------------------------------------------------------------------------------------"
echo ">>>>> Finished building catkin workspace"
echo "----------------------------------------------------------------------------------------------------"
