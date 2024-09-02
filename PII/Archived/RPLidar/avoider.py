#!/usr/bin/env python2.7

import rospy
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

#run export TURTLEBOT3_MODEL=waffle
#or
#run export TURTLEBOT3_MODEL=burger
#run roslaunch turtlebot3_gazebo turtlebot3_world.launch
#run roslaunch turtlebot3_gazebo turtlebot3_gazebo_rviz.launch
#run rosrun turtlebot3_movement move_avoid_obstacle.py 

#States
obstacle = False
left_obs = False #False -> right obstacle, True -> left obstacle
range_obs = 0.0
ort_obs = 0.0 #degrees
yaw = 0.0

#Scanner Specs
min_deg = -23 #degrees
max_deg = 23

def Angle2Index(laser_scan_msg, angle):
    return (int)((angle-laser_scan_msg.angle_min)/laser_scan_msg.angle_increment)

def Index2Angle(laser_scan_msg, index):
    return (laser_scan_msg.angle_min + (index*laser_scan_msg.angle_increment))

def isObstacleTooClose(range, min_view_deg, max_view_deg, dist_threshold):
    angle_inc = 0.017501922324299812 #radians
    min_view_idx = int(math.floor((min_view_deg/math.degrees(angle_inc))))
    max_view_idx = int(math.ceil((max_view_deg/math.degrees(angle_inc))))

    deg_left = range[0:max_view_deg]
    deg_right = range[len(arr_cleaned)+min_view_idx:359] + [arr_cleaned[len(arr_cleaned)-1]]
    sliced_arr = deg_left + deg_right
    # print(len(sliced_arr))
    # print(deg_left)
    # print(deg_right)
    if min(sliced_arr) < dist_threshold:
        idx = sliced_arr.index(min(sliced_arr))
        range = sliced_arr[idx]
        if (idx < len(sliced_arr)/2):
            ort_obs_deg = 360 - ((math.degrees(angle_inc))*((len(sliced_arr)/2)-idx))
            return True, True, range, ort_obs_deg  #true obstacle, true left_obs
        else:
            ort_obs_deg = math.degrees(angle_inc)*(idx-(len(sliced_arr)/2))
            return True, False, range, ort_obs_deg
    else:
        return False, False, 0.0, 0.0

def scan_cb(msg):
    global obstacle, left_obs, range_obs, ort_obs, min_deg, max_deg
    range=msg.ranges
    obstacle, left_obs, range_obs, ort_obs = isObstacleTooClose(range, min_deg, max_deg, 0.5) #optimized

def newOdom(msg):
    global yaw
    rot_q = msg.pose.pose.orientation
    roll, pitch, yaw = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    yaw = math.degrees(yaw)

if __name__ == '__main__' :
    arduino_port = '/dev/ttyACM0' 
    baud_rate = 9600  
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    rospy.init_node("move_avoid_obstacle",anonymous=True)
    scan_sub = rospy.Subscriber("/scan", LaserScan, scan_cb)
    odom_sub = rospy.Subscriber("/odom", Odometry, newOdom)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=100)
    loop_rate = rospy.Rate(10)
    cmd_vel_msg = Twist()
    
    # Without P Controller
    # while (not(rospy.is_shutdown())):
    #     if (obstacle):
    #         if (left_obs):
    #             print("obstacle on left found, turning right")
    #             cmd_vel_msg.linear.x = 0.0
    #             cmd_vel_msg.angular.z = -0.1
    #         else:
    #             print("obstacle on right found, turning left")
    #             cmd_vel_msg.linear.x = 0.0
    #             cmd_vel_msg.angular.z = 0.1
    #     else:
    #         print("safe")
    #         cmd_vel_msg.linear.x = 0.1
    #         cmd_vel_msg.angular.z = 0.0
        
    #     cmd_vel_pub.publish(cmd_vel_msg)
    #     loop_rate.sleep()

    # With P controller
    while (not(rospy.is_shutdown())):
        Kp_linear = 0.05
        Kp_angular = 0.8
        # print(f"yaw = {yaw}")
        obs_tolerance = 30 #degrees
        target_ort = 0.0
        if (obstacle):
            if (left_obs):
                print("obstacle on left found, turning right")
                cmd_vel_msg.linear.x = Kp_linear * range_obs
                command = "turnRight\n"  
                ser.write(command.encode())

                if target_ort == 0.0 :
                    target_ort = yaw - min_deg

                angle_err = abs( yaw-(target_ort - obs_tolerance) ) 

                # print(min_deg)
                # print(angle_err)

                cmd_vel_msg.angular.z = -Kp_angular * math.radians(angle_err)
            else:
                print("obstacle on right found, turning left")
                cmd_vel_msg.linear.x = Kp_linear * range_obs
                command = "turnLeft\n"  
                ser.write(command.encode())

                if target_ort == 0.0 :
                    target_ort = yaw + min_deg   

                angle_err = abs( (target_ort + obs_tolerance)-yaw ) 

                # print(max_deg)
                # print(angle_err)

                cmd_vel_msg.angular.z = Kp_angular * math.radians(angle_err)
        else:
            print("safe")
            target_ort = 0.0
            cmd_vel_msg.linear.x = 0.1
            cmd_vel_msg.angular.z = 0.0
            command = "foward\n"  
            ser.write(command.encode())
        
        cmd_vel_pub.publish(cmd_vel_msg)
        loop_rate.sleep()

