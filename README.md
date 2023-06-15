# camera_sim
Creating synthetic image data via Gazebo



## Install Gazebo

- [official tutorial](https://classic.gazebosim.org/tutorials?cat=install)
- May also need some [models](https://github.com/osrf/gazebo_models)



## Install camera_sim

- Clone camera_sim to the src directory under your ROS workspace
- Colcon build it



## Run camera_sim
Some environment variables may need to be configured
- GAZEBO_MODEL_PATH: your model directories
- GAZEBO_MODEL_DATABASE_URI: set to "" to avoid gazebo stucks on startup

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

