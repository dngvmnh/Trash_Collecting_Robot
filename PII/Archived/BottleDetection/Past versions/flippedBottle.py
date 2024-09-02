from imageai.Detection import ObjectDetection
import os
import cv2
import math
# Get the current working directory
execution_path = os.getcwd()
# Initialize the camera
cam = cv2.VideoCapture(0)
# Check if the camera is opened
if not cam.isOpened():
    print('cam is not opening')
    exit()
#Initializing variables
cnt = -1
def info(frame,object):
    """Calculate the angle and distance of the object from the frame."""
    endX = frame.shape[1]
    midY = int(frame.shape[0]//2)
    difY = midY - (object["box_points"][1] + object["box_points"][3])//2
    difX = endX - (object["box_points"][0] + object["box_points"][2])//2
    dX = endX - max(object["box_points"][0],object["box_points"][2])
    distanceX = (142.902*(math.e**(2.512*(dX/endX)))-132.985+400)
    if difX == 0:
        absAngle = 0
    else: 
        absAngle = math.atan(difY/difX)
    distance = distanceX/math.cos(absAngle)
    return int(math.degrees(absAngle)), int(distance)
def detect(frame):
    """Detect the object in the frame."""
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=80,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    for eachObject in detections:
        if eachObject['name']=='bottle':
            return eachObject
        
def center():
    """Adjust the camera to center the object."""
    adjust = True
    frc = 0
    while (adjust == True):
        frc += 1
        if (frc%30 == 0):
            ret, frame = cam.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            object = detect(frame)
            if (object):
                cv2.imshow('frame', frame)
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 10):
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
# Initialize the object detector
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\models\yolov3.pt"))
detector.loadModel()

while True:
    cnt += 1
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if (cnt%60==0):
        object = detect(frame)
        if object:
            print('Bottle detected with probability: {}%'.format(object["percentage_probability"]))
            print('Bottle {} mm away at an angle of {} degrees'.format(info(frame,object)[1], info(frame,object)[0]))
            center()
            # start_point = [object["box_points"][0], object["box_points"][1]]
            # end_point = [object["box_points"][2], object["box_points"][3]]
            # color = (255, 0, 0)  # Blue color in BGR
            # thickness = 2  # Line thickness of 2 px
            # frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        else:
            print('No bottle found')
    if not ret:
        break
    cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()