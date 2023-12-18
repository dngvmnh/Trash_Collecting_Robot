from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection import ObjectDetection
import os
import cv2


execution_path = os.getcwd()

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('cam is not opening')
    exit()
 
cnt = -1


def detect(frame):
    
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=60,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    for eachObject in detections:
        if eachObject['name'].lower()=='plastic-bottle':
            return eachObject

detector = CustomObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\model\model-training\models/tiny-yolov3_dataset_last.pt"))
detector.setJsonPath("BottleDetection\model\model-training\models\dataset_tiny-yolov3_detection_config.json")
detector.loadModel()

# detector = ObjectDetection()
# detector.setModelTypeAsYOLOv3()
# detector.setModelPath(os.path.join(execution_path, "BottleDetection\Current-versions\models\yolov3.pt"))
# detector.loadModel()
i = 0
while True:
    cnt += 1
    ret, frame = cam.read()
    if (cnt%1==0):
        object = detect(frame)
        if object:
            print('Bottle detected with probability: {}%'.format(object["percentage_probability"]))
            # center(object)
            start_point = [object["box_points"][0], object["box_points"][1]]
            end_point = [object["box_points"][2], object["box_points"][3]]
            
            # Blue color in BGR
            color = (255, 0, 0)
            
            # Line thickness of 2 px
            thickness = 2

            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        else:
            print(i)
            i+=1
    if not ret:
            break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()