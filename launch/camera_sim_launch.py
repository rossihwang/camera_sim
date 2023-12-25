
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchService
from launch.actions import ExecuteProcess, GroupAction, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node, PushRosNamespace
from json import load


def generate_launch_description():

    configs = None
    sensor_sim_dir = get_package_share_directory("sensor_sim")
    default_config_file = os.path.join(sensor_sim_dir, "configs", "stereo.json")

    with open(default_config_file, "r") as f:
        configs = load(f)

    cameras = []

    world = configs["world"]
    world_file = os.path.join(sensor_sim_dir, "world",
                              world+".world") if world else ""

    for c in configs["cameras"]:
        sdf_file = os.path.join(sensor_sim_dir, "models", c["model"]+".sdf")
        cameras.append(
            {
              "model": c["model"],
              "namespace": c["namespace"],
              "x": float(c["position"][0]),
              "y": float(c["position"][1]),
              "z": float(c["position"][2]),
              "R": float(c["orientation"][0]),
              "P": float(c["orientation"][1]),
              "Y": float(c["orientation"][2]),
              "sdf": sdf_file
            }
        )
    print(cameras)

    master_uri = master_uri if configs["master_uri"] else ""
    os.environ["GAZEBO_MASTER_URI"] = master_uri
    start_gzserver_cmd = ExecuteProcess(
        cmd = ["gzserver", "-s", "libgazebo_ros_factory.so", "--minimal_comms", world_file],
        output = "screen"
    )

    spawn_cmds = []
    for c in cameras:
        spawn_cmds.append(
            Node(
              package="gazebo_ros",
              executable="spawn_entity.py",
              output="screen",
              arguments=[
                "-file", TextSubstitution(text=c["sdf"]),
                "-entity", TextSubstitution(text=c["namespace"]+"_"+c["model"]),
                "-robot_namespace", TextSubstitution(text=c["namespace"]),
                "-x", TextSubstitution(text=str(c["x"])),
                "-y", TextSubstitution(text=str(c["y"])),
                "-z", TextSubstitution(text=str(c["z"])),
                "-R", TextSubstitution(text=str(c["R"])),
                "-P", TextSubstitution(text=str(c["P"])),
                "-Y", TextSubstitution(text=str(c["Y"]))
              ]
            )
        )

    ld = LaunchDescription()
    # ld.add_action(SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1"),)
    # ld.add_action(SetEnvironmentVariable("REUTILS_LOGGING_USE_STDOUT", "1"),)
    ld.add_action(start_gzserver_cmd)
    for cmd in spawn_cmds:
        ld.add_action(cmd)

    return ld
