# ros2_msg_sphinx

A sphinx extension which displays ROS message definitions plus their documentation extracted from comments.

This is very WIP!

## Usage
* Add this (as a submodule if you want) at `doc/_ext/ros2_msg_sphinx`
* Enable the plugin in your sphinx `config.py`:
```python
sys.path.append(os.path.abspath("./_ext/ros2_msg_sphinx"))
extensions = [..., "ros_msg"]
```

* Add a `rosmessage` directive in some part of your docs (rst):
```rst
.. rosmessage:: /home/jonas/workspace/rviz_2d_overlay_plugins/rviz_2d_overlay_msgs/msg/OverlayText.msg
   :pkg_name: rviz_2d_overlay_msgs
   :msg_name: OverlayText 
```
yes it currently requires the absolute path, thats why i said "WIP" earlier :D
