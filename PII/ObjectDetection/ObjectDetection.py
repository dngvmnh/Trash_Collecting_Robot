from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
# detector.setModelPath( os.path.join(execution_path , "Old_PII/ObjectDetection/resnet50_coco_best_v2.0.1.h5"))
detector.setModelPath( os.path.join(execution_path , "PII_Projects/Old_PII/PII_Robot/BottleDetection/models/yolov3.pt"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"), extract_detected_objects=True)
for eachObject in detections:
    print(eachObject['name'] + " : " + eachObject['percentage_probability'] )
