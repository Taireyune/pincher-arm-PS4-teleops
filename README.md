# Pincher-Arm-PS4-Teleops
<img 
src="https://github.com/Taireyune/pincher-arm-PS4-teleops/blob/main/images/communications_circled.png" 
width="500" height="380" alt="relationship">

## Overview
This project contains the python scripts for manually controlling the [pincher arm](https://github.com/Taireyune/pincher-arm) using ROS messages.
The controls correspond to the motor pwm for each joint. A crude version of the video feed can be used to watch the arm movements.

## Usage
- compile and add [cortex-message-handling](https://github.com/Taireyune/cortex-message-handling) to be to path.
- pip install rospy, zmq, numpy, cv2, inputs
