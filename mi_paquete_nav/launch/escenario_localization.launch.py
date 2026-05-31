import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg = get_package_share_directory('mi_paquete_nav')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    world = os.path.join(pkg, 'worlds', 'escenario.sdf')
    params = os.path.join(pkg, 'params', 'nav2_params.yaml')
    map_file = os.path.join(pkg, 'maps', 'mi_mapa.yaml')

    set_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(pkg, 'models')
    )

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'tb3_simulation_launch.py')
        ),
        launch_arguments={
            'world': world,
            'params_file': params,
            'map': map_file,          # <-- el mapa guardado
            'slam': 'False',          # <-- localización con AMCL, no SLAM
            'use_sim_time': 'True',
            'headless': 'False',
        }.items()
    )

    return LaunchDescription([
        set_resource_path,
        sim,
    ])