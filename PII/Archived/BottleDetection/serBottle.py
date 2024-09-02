from imageai.Detection import ObjectDetection
import os
import cv2
import math
import serial
ser = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

execution_path = os.getcwd()
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    ser.write('e')
    exit()

# Initialize the object detector
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\models\yolov3.pt"))
detector.loadModel()
def info(frame,object):
    endX = frame.shape[1]
    midY = int(frame.shape[0]//2)
    difY = midY - (object["box_points"][1] + object["box_points"][3])//2
    difX = endX - (object["box_points"][0] + object["box_points"][2])//2
    dX = endX - max(object["box_points"][0],object["box_points"][2])
    distanceX = (142.902*(math.e**(2.512*(dX/endX)))-132.985+400)
    absAngle = 0 if difX == 0 else math.atan(difY/difX)
    distance = distanceX/math.cos(absAngle)
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

def center(frame):
    # 1: fl 3: nl 5: c 7: nr 9: fr
    # 2: bw 4: tl 6: tr 8: fw 0: stop
    # r: object out of frame (slowly turn around)
    # n: no object found, cont going

    frc = 0
    while True:
        ser.write(0)
        frc += 1
        if (frc%60 == 0):
            ret, frame = cam.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            object = detect(frame)
            if (object):
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 10):
                    ser.write(b'5')
                    return
                elif (angle < -45):
                    ser.write(b'9')
                elif (angle < 0):
                    ser.write(b'7')
                elif (angle < 45):
                    ser.write(b'3')
                else:
                    ser.write(b'1')
            else:
                ser.write(b'r')
            waitForExecution()
            if not ret:
                break
def main():   
    cnt = -1
    while True:
        ser.write(0)
        cnt += 1
        if (cnt%60==0):
            ret, frame = cam.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            object = detect(frame)
            if object:
                print('Bottle found')
                ser.write('bottle found')
                center(frame)
            else:
                ser.write(b'n')
        if not ret:
            break
        if cv2.waitKey(1)==ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()