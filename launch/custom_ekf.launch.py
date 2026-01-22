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

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    ekf_node = launch_ros.actions.Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',

        # ---------------------------------------------------------
        # 1. NAMESPACE: Sets the scope to /<robot_name>
        # ---------------------------------------------------------
        namespace=robot_name,

        parameters=[
            # Path to the YAML file
            os.path.join(get_package_share_directory("robot_localization"), 'params', 'ekf_sim.yaml'),
            {'use_sim_time': use_sim_time}
        ],

        # ---------------------------------------------------------
        # 2. REMAPPING: ('/tf', 'tf') becomes '/<robot_name>/tf'
        # ---------------------------------------------------------
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    return LaunchDescription([
        robot_name_arg,
        use_sim_time_arg,
        ekf_node
    ])

