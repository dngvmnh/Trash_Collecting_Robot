#!/usr/bin/env python2.7

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
from rplidar import RPLidar

SAFE_DISTANCE = 450

def get_angle_range(start_angle, end_angle):
    angle_range = end_angle - start_angle
    if angle_range < 0:
        angle_range += 360
    return angle_range

def find_obstacles(scan_data, safe_distance):
    obstacles = []
    for angle, distance in scan_data:
        if distance <= safe_distance:
            obstacles.append((angle, distance))
    return obstacles

def choose_navigation_direction(obstacles):
    if not obstacles:
        return 0  
    max_obstacle_angles = max(obstacles, key=lambda t: t[1])
    obstacle_angles=max_obstacle_angles[0]
    chosen_direction = 0
    if obstacle_angles > 0 and obstacle_angles < 45 :
        chosen_direction = obstacle_angles 
    elif obstacle_angles < 360 and obstacle_angles > 315 :
        chosen_direction = obstacle_angles 
    return chosen_direction

def calculate_distance_to_obstacle(scan_data, target_angle):
    for angle, distance in scan_data:
        if angle == target_angle:
            return distance
    return None

def main():
    rospy.init_node("obstacle_avoidance_node", anonymous=True)

    lidar = RPLidar('/dev/ttyUSB0')  
    lidar.start_motor()
    arduino_port = '/dev/ttyACM0'  
    ser = serial.Serial(arduino_port, 9600, timeout=1)

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    try:
        while not rospy.is_shutdown():
            scan_data = [(entry[1], entry[2]) for entry in lidar.iter_scans()]

            obstacles = find_obstacles(scan_data, SAFE_DISTANCE)

            chosen_direction = choose_navigation_direction(obstacles, MAX_TURN_ANGLE)

            distance_to_obstacle = calculate_distance_to_obstacle(scan_data, chosen_direction)

            cmd_vel_msg = Twist()
        if not obstacles:
                print("Safe - No obstacle ")
                command = "forward\n"
                cmd_vel_msg.linear.x = 0.2
        else:
                if chosen_direction < 360 and chosen_direction > 315 :
                    print("Turning Left - Obstacle detected on the right")
                    command = "turnLeft\n"
                    cmd_vel_msg.angular.z = 0.5 
                elif chosen_direction > 0 and chosen_direction < 45 :
                    print("Turning Right - Obstacle detected on the left")
                    command = "turnRight\n"
                    cmd_vel_msg.angular.z = -0.5
                else:
                    print("Safe - No obstacle ")
                    command = "forward\n"
                    cmd_vel_msg.linear.x = 0.2
  
        ser.write(command.encode())
                

        pub.publish(cmd_vel_msg)
        rate.sleep()

    except rospy.ROSInterruptException:
        pass

    finally:
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == "__main__":
    main()
