# Copyright 2018 Open Source Robotics Foundation, Inc.
# Copyright 2019 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import launch_ros.actions
import os
import yaml
from launch.substitutions import EnvironmentVariable
import pathlib
import launch.actions
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # 1. Create a variable for the robot's name
    robot_name = LaunchConfiguration('robot_name')

    # 2. Declare the argument (defaults to 'kevin' for testing)
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='kevin',
        description='Name of the robot (namespace)'
    )

    return LaunchDescription([
        robot_name_arg,
        
        launch_ros.actions.Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            # ---------------------------------------------------------
            # 1. NAMESPACE: Sets the scope to /<robot_name>
            # ---------------------------------------------------------
            namespace=robot_name,
            
            parameters=[os.path.join(get_package_share_directory("robot_localization"), 'params', 'ekf.yaml')],
            
            # ---------------------------------------------------------
            # 2. REMAPPING: ('/tf', 'tf') becomes '/<robot_name>/tf'
            # ---------------------------------------------------------
            remappings=[('/tf', 'tf')] 
        ),
    ])

