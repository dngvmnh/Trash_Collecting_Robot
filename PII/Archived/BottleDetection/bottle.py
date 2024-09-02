
from imageai.Detection import ObjectDetection
import os
import cv2
import math 


execution_path = os.getcwd()

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('cam is not opening')
    exit()
 
cnt = -1

def info(frame,object):
    endY = frame.shape[0]
    midX = int(frame.shape[1]//2)
    difX = midX - (object["box_points"][0] + object["box_points"][2])//2
    difY = endY - (object["box_points"][1] + object["box_points"][3])//2
    dY = endY - max(object["box_points"][1],object["box_points"][3])
    #formula
    distanceY = (142.902*(math.e**(2.512*(dY/endY)))-132.985+400)
    if difY == 0:
         absAngle = 0
    else: absAngle = math.atan(difX/difY)
    distance = distanceY/math.cos(absAngle)
    return int(math.degrees(absAngle)), int(distance)

def detect(frame):
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    for eachObject in detections:
        if eachObject['name']=='bottle':
            return eachObject

def center(object):
    adjust = True
    frc = 0
    while (adjust == True):
        frc += 1
        if (frc%90 == 0):
            ret, frame = cam.read()
            object = detect(frame)
            if (object):
                cv2.imshow('frame', frame)
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 5):
                    print('centered')
                    adjust = False
                elif (angle < -45):
                    print('far right')
                elif (angle < 0):
                    print('near right')
                elif (angle < 45):
                    print('near left')
                else:
                    print('far left')
            else:
                print('Object out of frame')
    print ('Bottle {} mm away, centered'.format(info(frame,object)[1], info(frame,object)[0]))
    print("--------------------------------")

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "PII_Projects/Old_PII/PII_Robot/BottleDetection/models/yolov3.pt"))
detector.loadModel()

while True:
    cnt += 1
    ret, frame = cam.read()
    if (cnt%30==0):
        object = detect(frame)
        if object:
            print('Bottle detected with probability: {}%'.format(object["percentage_probability"]))
            print('Bottle {} mm away at an angle of {} degrees'.format(info(frame,object)[1], info(frame,object)[0]))
            center(object)
        else:
            print('No bottle found')
    if not ret:
            break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()