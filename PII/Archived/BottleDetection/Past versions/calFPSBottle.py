from imageai.Detection import ObjectDetection
import os
import cv2
import math
import time
 # Get the current working directory
execution_path = os.getcwd()
 # Initialize the camera
cam = cv2.VideoCapture(0)
 # Check if the camera is opened
if not cam.isOpened():
    print('cam is not opening')
    exit()
 # Initialize the object detector
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\models\yolov3.pt"))
detector.loadModel()
def info(frame,object):
    """Calculate the angle and distance of the object from the frame."""
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
    """Detect the object in the frame."""
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=80,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    return next((eachObject for eachObject in detections if eachObject['name']=='bottle'), None)

def center(frame):
    """Adjust the camera to center the object."""
    frc = 0
    while True:
        frc += 1
        ret, frame = cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if (frc%30 == 0):
            object = detect(frame)
            if (object):
                cv2.imshow('frame', frame)
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 10):
                    print('centered')
                    return
                print('Current angle: {} '.format(str(angle)) + ('far right' if angle < -45 else 'near right' if angle < 0 else 'near left' if angle < 45 else 'far left'))
            else:
                print('Object out of frame')
        if not ret:
            break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    

cnt = -1
while True:
    startTime = time.time()
    cnt += 1
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if (cnt%30==0):
        object = detect(frame)
        print("Detecting FPS rate: ", 1.0 / (time.time() - startTime))
        if object:
            print('Bottle {} mm away at an angle of {} degrees'.format(info(frame,object)[1], info(frame,object)[0]))
        else:
            print('No bottle found')
    else:
        print("FPS: ", 1.0 / (time.time() - startTime))
    if not ret:
        break
    cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()