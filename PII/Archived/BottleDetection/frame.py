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
        if (frc%30 == 0):
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
    if object:
        start_point = (object["box_points"][0], object["box_points"][1])
        end_point = (object["box_points"][2], object["box_points"][3])
        color = (0, 255, 255)  # Yellow color in BGR (OpenCV uses BGR format)
        thickness = 2  # Line thickness of 2 px

        # Draw a rectangle (yellow frame) around the detected bottle
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

        # Display the detection percentage on the frame
        percentage = object["percentage_probability"]
        text = f"Bottle: {percentage:.2f}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_x = start_point[0] + 5
        text_y = start_point[1] - text_size[1] - 5
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, font_thickness)

        cv2.imshow('frame', frame)
    else:
        print('Object out of frame')

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\models\yolov3.pt"))
detector.loadModel()

while True:
    cnt += 1
    ret, frame = cam.read()
    if (cnt%60==0):
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