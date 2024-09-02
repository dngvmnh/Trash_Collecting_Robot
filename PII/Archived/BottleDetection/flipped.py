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

#calculate distance and angle based on found formula
def distance(frame,object):
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    endY = frame.shape[0]
    midX = int(frame.shape[1]//2)
    difX = midX - (object["box_points"][0] + object["box_points"][2])//2
    difY = endY - (object["box_points"][1] + object["box_points"][3])//2
    dY = endY - max(object["box_points"][1],object["box_points"][3])
    distanceY = (142.902*(math.e**(2.512*(dY/endY)))-132.985+400)
    if difY == 0:
         absAngle = 0
    else: absAngle = math.atan(difX/difY)
    distance = distanceY/math.cos(absAngle)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return int(math.degrees(absAngle)), int(distance)

def position(frame,object):
    angle = distance(frame,object)[0]
    if (abs(angle)<=5):
        return 'centered'
    #if object is on the left-hand side
    elif angle > 0: 
        return 'turn left'
    elif angle < 0:
        return 'turn right'
    
def center(object):
    adjust = True
    while (adjust == True):
        frame = cam.read()
        msg = position(frame, object)
        if (msg == 'centered'):
            adjust = False
        else:
            #adjust robot
            print('')

while True:
    cnt += 1
    ret, frame = cam.read()
    frame= cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if (cnt%15==0):
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path, "BottleDetection\models\yolov3.pt"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)

        for eachObject in detections:
            if eachObject['name']=='bottle':
                print ('Object {} mm away at an angle of {} degrees'.format(distance(frame,eachObject)[1], distance(frame,eachObject)[0]))
                position(frame,eachObject)
                print('Bottle detected with probability: {}%'.format(eachObject["percentage_probability"]))
                print("--------------------------------")
                
                # start_point = [eachObject["box_points"][0], eachObject["box_points"][1]]
                # end_point = [eachObject["box_points"][2], eachObject["box_points"][3]]
                # color = (255, 0, 0)
                # thickness = 2
                # frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                

    if not ret:
            break

    cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()