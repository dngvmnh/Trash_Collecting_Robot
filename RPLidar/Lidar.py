import math
import time
from rplidar import RPLidar
import serial

SAFE_DISTANCE = 550
TOP_SAFE_DISTANCE = 350
BOT_SAFE_DISTANCE = 250

def get_angle_range(start_angle, end_angle):
    angle_range = end_angle - start_angle
    if angle_range < 0:
        angle_range += 360
    return angle_range

def find_obstacles(scan_data, safe_distance):
    obstacles = []
    for angle, distance in scan_data:
        if (distance <= safe_distance and angle <= 360 and angle > 315) or (distance <= safe_distance and angle < 45 and angle >= 0):
            obstacles.append((angle, distance))
    return obstacles

def choose_navigation_direction(obstacles):
    if not obstacles:
        return 0  
    min_obstacle_angles = min(obstacles, key=lambda t: t[1])
    obstacle_angles=min_obstacle_angles[0]
    chosen_direction = 0
    if obstacle_angles >= 0 and obstacle_angles <= 45 :
        chosen_direction = obstacle_angles 
    elif obstacle_angles <= 360 and obstacle_angles >= 315 :
        chosen_direction = obstacle_angles 
    return chosen_direction

def calculate_distance_to_obstacle(scan_data, target_angle):
    for angle, distance in scan_data:
        if angle == target_angle:
            return distance
    return distance

if __name__ == "__main__":
    lidar = RPLidar('COM10') 
    lidar.start_motor()
    arduino_port = 'COM11'  
    ser = serial.Serial(arduino_port, 9600, timeout=1)

    try:
        for scan in lidar.iter_scans():
            scan_data = [(entry[1], entry[2]) for entry in scan]
            
            obstacles = find_obstacles(scan_data, SAFE_DISTANCE)

            chosen_direction = choose_navigation_direction(obstacles)

            distance_to_obstacle = calculate_distance_to_obstacle(scan_data, chosen_direction)

            ser.write(b'forward\n')

            if not obstacles:
                print("Safe - No obstacle ")
                ser.write(b'0')
                ser.write(b'forward\n')
            if (chosen_direction > 351 and chosen_direction <= 360) or (chosen_direction > 0 and chosen_direction <= 9):
                print("Rotate Left - Obstacle on the Front")
                ser.write(b'0')
                ser.write(b'rotateLeft\n')
            if (chosen_direction > 9 and chosen_direction <= 27 and distance_to_obstacle < TOP_SAFE_DISTANCE)  :
                print("Turning Right - Obstacle detected on the topRight")
                ser.write(b'0')
                ser.write(b'rotateLeft\n')
            if (chosen_direction > 27 and chosen_direction <= 45 and distance_to_obstacle < BOT_SAFE_DISTANCE)  :
                print("Turning Right - Obstacle detected on the botRight")
                ser.write(b'0')
                ser.write(b'rotateLeft\n')
            if (chosen_direction > 333 and chosen_direction <= 351 and distance_to_obstacle < TOP_SAFE_DISTANCE) :
                print("Turning Left - Obstacle detected on the topLeft")
                ser.write(b'0')
                ser.write(b'rotateRight\n')
            if (chosen_direction > 315 and chosen_direction <= 333 and distance_to_obstacle < BOT_SAFE_DISTANCE) :
                print("Turning Left - Obstacle detected on the botLeft")
                ser.write(b'0')
                ser.write(b'rotateRight\n')
            # if chosen_direction > 45 and chosen_direction < 315:
            #     print("Safe - No obstacle ")
            #     ser.write(b'0')
            #     ser.write(b'forward\n')

    except KeyboardInterrupt:
        pass

    lidar.stop_motor()
    lidar.disconnect()
