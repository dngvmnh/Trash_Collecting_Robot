import math
import time
from rplidar import RPLidar
import serial
from imageai.Detection import ObjectDetection
import os
import cv2
import threading

execution_path = os.getcwd()
cam = cv2.VideoCapture(0)

bottleFound = False
bottleCollected  = False
arduino_port = 'COM13'
lidar_port = 'COM10'
# arduino_port = '/dev/ttyACM0'
# lidar_port = '/dev/ttyUSB0'
ser = serial.Serial(arduino_port, 9600)
if not cam.isOpened():
    print('error opening camera')
    exit()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "PII-robot/BottleDetection/Current-versions/models/yolov3.pt"))
detector.loadModel()

SAFE_DISTANCE = 550
TOP_SAFE_DISTANCE = 350
BOT_SAFE_DISTANCE = 250

def info(frame,object):
    endX = frame.shape[1]
    midY = int(frame.shape[0]//2)
    difY = midY - (object["box_points"][1] + object["box_points"][3])//2
    difX = endX - (object["box_points"][0] + object["box_points"][2])//2
    dX = endX - max(object["box_points"][0],object["box_points"][2])
    distanceX = (309.059*(math.e**(1.04215*(dX/endX)))+130.13)/10
    absAngle = 0 if difX == 0 else math.atan(difY/difX)
    distance = distanceX/math.cos(absAngle)
    print(f"Distance: {distance} cm")
    return int(math.degrees(absAngle)), int(distance)

def detect(frame):
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=80,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    return next((eachObject for eachObject in detections if eachObject['name']=='bottle'), None)

def waitForExecution():
    while True:
                data = ser.readline().decode().strip()
                if (data.lower()=='done executing'):
                    break

def center():
    frc = 0
    while True:
        ser.write(0)
        frc += 1
        ret, frame = cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if (frc%2==0):
            object = detect(frame)
            if (object):
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 10):
                    print('centered')
                    return
                print(f'Current angle: {angle} ')
                msg = ('farRight' if angle > 45 else 'nearRight' if angle > 0 else 'nearLeft' if angle > -45 else 'farLeft') + '\n'
            else:
                msg = 'outFrame\n'
            ser.write(msg.encode('utf-8'))
            print(msg)
            waitForExecution()
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
        cv2.waitKey(1)

def runTo():
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    object = detect(frame)
    if (object):
        distance = info(frame, object)[1]
        ser.write(b'forward\n')
        time.sleep(distance/40)
        ser.write(b'stop\n')
    else:
        runTo()

def mainCamera():
    print('camera') 
    cnt = -1
    while True:
        ret, frame = cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        ser.write(0)
        cnt += 1
        if (cnt%2==0):
            object = detect(frame)
            if object:
                print('Bottle found')
                center()
                runTo()
            else:
                print('No bottle found')
        if not ret:
            break
        if cv2.waitKey(1)==ord('q'):
            break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
        cv2.waitKey(1)
    cam.release()
    cv2.destroyAllWindows()

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

current_msg = ''
last_msg = ''

def lidar():
    lidar = RPLidar(lidar_port) 
    lidar.start_motor() 

    try:
        for scan in lidar.iter_scans():
            scan_data = [(entry[1], entry[2]) for entry in scan]
            
            obstacles = find_obstacles(scan_data, SAFE_DISTANCE)

            chosen_direction = choose_navigation_direction(obstacles)

            distance_to_obstacle = calculate_distance_to_obstacle(scan_data, chosen_direction)

            ser.write(b'forward\n')

            if not obstacles:
                print("Safe - No obstacle ")
                current_msg = 'forward\n'
            elif (chosen_direction > 351 and chosen_direction <= 360) or (chosen_direction > 0 and chosen_direction <= 9):
                print("Rotate Left - Obstacle on the Front")
                current_msg = 'rotateLeft\n'
            elif (chosen_direction > 9 and chosen_direction <= 27 and distance_to_obstacle < TOP_SAFE_DISTANCE)  :
                print("Turning Right - Obstacle detected on the topRight")
                current_msg = 'rotateRight\n'
            elif (chosen_direction > 27 and chosen_direction <= 45 and distance_to_obstacle < BOT_SAFE_DISTANCE)  :
                print("Turning Right - Obstacle detected on the botRight")
                current_msg = 'rotateRight\n'
            elif (chosen_direction > 333 and chosen_direction <= 351 and distance_to_obstacle < TOP_SAFE_DISTANCE) :
                print("Turning Left - Obstacle detected on the topLeft")
                current_msg = 'rotateLeft\n'
            elif (chosen_direction > 315 and chosen_direction <= 333 and distance_to_obstacle < BOT_SAFE_DISTANCE) :
                print("Turning Left - Obstacle detected on the botLeft")
                current_msg = 'rotateLeft\n'
            # if chosen_direction > 45 and chosen_direction < 315:
            #     print("Safe - No obstacle ")
            #     ser.write(b'0')
            #     ser.write(b'forward\n')
            if current_msg != last_msg:
                ser.write(b'0')
            ser.write(current_msg.encode('utf-8'))
            last_msg = current_msg

    except KeyboardInterrupt:
        pass

    lidar.stop_motor()
    lidar.disconnect()

def movement():
    while True:
        lidar()

if __name__ == '__main__':
    thr1 = threading.Thread(target = mainCamera)
    thr2 = threading.Thread(target = movement)
    thr1.start()
    time.sleep(10)
    thr2.start()
    thr1.join()
    thr2.join()
