import cv2

while True:
    port = int(input('Port: '))
    cam = cv2.VideoCapture(port)
    if not cam.isOpened():
        print('cam is not opened')
    else:
        ret, frame = cam.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
cam.release()
cv2.destroyAllWindows()