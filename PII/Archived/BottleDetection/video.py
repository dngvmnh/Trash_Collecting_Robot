import cv2 as cv
import numpy as np

#para=0:webcam, 1:intecam
cam = cv.VideoCapture(0)
result, image = cam.read()

def cvvideo():
    if not cam.isOpened():
        exit()
    while True:
        ret, frame = cam.read()

        if not ret:
            break

        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()
cvvideo()