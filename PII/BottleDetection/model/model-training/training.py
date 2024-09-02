# from imageai.Detection.Custom import DetectionModelTrainer

# trainer = DetectionModelTrainer()
# trainer.setModelTypeAsTinyYOLOv3()
# trainer.setDataDirectory(data_directory="BottleDetection/model/model-training/new-btl-dts")
# trainer.setTrainConfig(object_names_array=["Plastic-Bottle"], batch_size=4, num_experiments=100, train_from_pretrained_model="BottleDetection/model/model-training/new-btl-dts/models/BottleDetection/model/model-training/new-btl-dts/models/tiny-yolov3_new-btl-dts_last.pt")
# trainer.trainModel()


from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="hololens-yolo")
trainer.setTrainConfig(object_names_array=["hololens"], batch_size=4, num_experiments=200, train_from_pretrained_model="Old_PII/PII_Robot/BottleDetection/models/yolov3.pt")
# In the above,when training for detecting multiple objects,
#set object_names_array=["object1", "object2", "object3",..."objectz"]
trainer.trainModel()