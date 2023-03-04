# camera_sim
Creating synthetic image data via Gazebo



## Install Gazebo

- [official tutorial](https://classic.gazebosim.org/tutorials?cat=install)
- May also need some [models](https://github.com/osrf/gazebo_models)



## Install camera_sim

- Clone camera_sim to the src directory under your ROS workspace
- Colcon build it



## Run camera_sim

```shell
ros2 launch camera_sim camera_sim_launch.py # run a gzserver
```

In another terminal

```shell
gzclient
```



## Capture data



## Lable the data

- CVAT

