import math
import time
from rplidar import RPLidar
import serial

SAFE_DISTANCE = 600  # millimeters

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
    max_obstacle_angles = min(obstacles, key=lambda t: t[1])
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
    return distance

if __name__ == "__main__":
    lidar = RPLidar('COM10') 
    lidar.start_motor()
    # arduino_port = 'COM11'  
    # ser = serial.Serial(arduino_port, 9600, timeout=1)

    while True:
        for scan in lidar.iter_scans():
            scan_data = [(entry[1], entry[2]) for entry in scan]
            
            obstacles = find_obstacles(scan_data, SAFE_DISTANCE)

            chosen_direction = choose_navigation_direction(obstacles)

            distance_to_obstacle = calculate_distance_to_obstacle(scan_data, chosen_direction)

            if not obstacles:
                print("Safe - No obstacle ")
            else:
                if chosen_direction < 360 and chosen_direction > 315 :
                    print("Turning Right - Obstacle detected on the left")
                elif chosen_direction > 0 and chosen_direction < 45 :
                    print("Turning Left - Obstacle detected on the right")
                else:
                    print("Safe - No obstacle ")


    # except KeyboardInterrupt:
    #     pass

    # lidar.stop_motor()
    # lidar.disconnect()
