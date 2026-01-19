from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Static TF: base_link -> imu_link
        # Args: x y z yaw pitch roll parent_frame child_frame
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_imu_tf_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'imu_link'],
            output='screen'
        ),

        # Static TF: base_link -> dvl_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_dvl_tf_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'dvl_link'],
            output='screen'
        )
    ])