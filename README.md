## DEMO
**1. Avoiding Obstacle**

https://github.com/dngvmnh/Trash_Collecting_Robot/assets/133772077/0d24710b-7814-45a0-8826-957f754a2fe8

**2. Collecting Trash**

https://github.com/dngvmnh/Trash_Collecting_Robot/assets/133772077/7494913d-235f-4eb4-9d58-ff773b87debb

## Project Description

**1. Overview**

This is an autonomous bottle-collecting robot that uses computer vision to detect bottles and lidar algorithms to avoid obstacles. Plastic trash pollution is on the rise in modern times, with alarming consequences for the environment. However, using the present automatic trash-collecting robots on the market is challenging and intricate. Previous deployments of automated systems for the same task had not been optimized in terms of cost and hardware. After designing, simulating obstacle avoidance algorithms, and retraining the object detection model, the aim of this research is to enhance and develop a more efficient robotic system. Its results can be applied to subsequent research in the same field.

**2. The PII program**

This research project is carried out as part of the PTNK Innovation Initiative (PII) Summer Research Internship Program under the topic "4d. Smart Robot" at Makerspace - Fulbright University Vietnam from June 15, 2023, to September 5, 2023. The program is established and ran by PTNK (VNU-HCM High School for the Gifted) STEAM Club.

## Implementation

The implementation of this robot includes three main stages: designing its mechanics, assembling electronic components, and establishing its software.

● The 3D design file can be found here: [Design folder](https://github.com/dngvmnh/Trash_Collecting_Robot/tree/main/Robot_Design).

● Arduino Uno and Jetson Nano were used as controllers; DC motors as actuators; and an RPLidar and webcam as sensors.

● There are three main programs for this robot: bottle detection, obstacle avoidance, and controlling the motors. Arduino Uno and Jetson Nano communicate through the serial port. Bottle detection and obstacle avoidance algorithms are joined by multi-threading. For optimizing the object detection model, the TinyYoloV3 was trained with an available dataset. An equation for calculating the distance to a bottle from the camera's image is formed.

For more details, refer to this repository: [Arduino](https://github.com/dngvmnh/Trash_Collecting_Robot/tree/main/Arduino), [Bottle Detection](https://github.com/dngvmnh/Trash_Collecting_Robot/tree/main/Bottle_Detection).

## Results and discussion

A robot system capable of navigating, detecting bottles, and avoiding obstacles with a price range of $341 to $400 was successfully deployed. This result fits the initial scope of this project. However, the Jetson Nano's processing speed and object detection model's rate are still relatively slow; the lidar can be optimized with the implementation of ROS SLAM simulation. In addition, the robot's electronic components are not covered, making them susceptible to damage and malfunction. Future research should focus on resolving these proposed issues.

Images and videos of this robot can be found here: [Media](https://github.com/dngvmnh/Trash_Collecting_Robot/tree/main/Results/Media).

## Report

For further information, refer to this report: [View on GitHub](https://github.com/dngvmnh/Trash_Collecting_Robot/blob/main/Results/Report/PII%20-%20Report%20-%20FUV.pdf) or [Download PDF](https://github.com/dngvmnh/Trash_Collecting_Robot/raw/main/Results/Report/PII%20-%20Report%20-%20FUV.pdf).
