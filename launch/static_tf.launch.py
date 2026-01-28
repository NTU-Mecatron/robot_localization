from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )    

    return LaunchDescription([
        use_sim_time_arg,

        # ---------------------------------------------------------
        # Static TF: base_link -> imu_link
        # Translation: 
        #   X = +0.10576 m (105.76mm Forward)
        #   Y = 0
        #   Z = +0.095 m   (95mm Above)
        # ---------------------------------------------------------
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_imu_tf_publisher',
            arguments=['0.10576', '0', '0.095', '0', '0', '0', 'base_link', 'imu_link'],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        ),

        # ---------------------------------------------------------
        # Static TF: base_link -> dvl_link
        # Translation:
        #   X = 0
        #   Y = 0
        #   Z = -0.11115 m (111.15mm Below)
        # ---------------------------------------------------------
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_dvl_tf_publisher',
            arguments=['0', '0', '-0.11115', '0', '0', '0', 'base_link', 'dvl_link'],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )
    ])