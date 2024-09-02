# Import libraries
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import glob
import yaml
import os

path = os.getcwd()
images = glob.glob('Bottle Detection/images/*.jpg')
cam = cv.VideoCapture(0)

# Define the number of corners in the chessboard pattern
CHESSBOARD_CORNER_NUM_X = 7
CHESSBOARD_CORNER_NUM_Y = 6

# Define the output file for the camera parameters
CAMERA_PARAMETERS_OUTPUT_FILE = "cam1.yaml"

# Define the termination criteria for corner detection
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
# The Z-coordinate is 0 because the chessboard is assumed to lie in the XY plane
objp = np.zeros((CHESSBOARD_CORNER_NUM_X*CHESSBOARD_CORNER_NUM_Y,3), np.float32)
objp[:,:2] = np.mgrid[0:CHESSBOARD_CORNER_NUM_X,0:CHESSBOARD_CORNER_NUM_Y].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Loop over all the images in the specified directory
for fname in images:
    # Load the image and convert it to grayscale
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (CHESSBOARD_CORNER_NUM_X,CHESSBOARD_CORNER_NUM_Y), None)
    
    # Define the corners
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (CHESSBOARD_CORNER_NUM_X,CHESSBOARD_CORNER_NUM_Y), corners2, ret)
        

    else:
        print('Failed to find a chessboard in {}'.format(fname))

# Return the camera matrix
ret, camMatrix, distortionCoeff, rotationVectors, translationVectors = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

# Displaying required output
print("\nCamera matrix:\n", camMatrix)
print("\nDistortion Parameters:\n", distortionCoeff)

# Extract the focal length in pixels from the camera's intrinsic matrix
fx_pix = int(camMatrix[0][0])
fy_pix = int(camMatrix[1][1])

# Print the focal length in pixels
print("fx in pixel: ", fx_pix)
print("fy in pixel: ", fy_pix)

# Get the image height, image width, and number of channels
img_h, img_w, channel = img.shape

# Set the camera sensor width (in mm)
sensor_width = 3.58

# Convert the focal length from pixels to mm
fx_mm = fx_pix * sensor_width / img_w
fy_mm = fy_pix * sensor_width / img_w

# Print the focal length in mm
print("fx in mm: ", round(fx_mm,2))
print("fy in mm: ", round(fy_mm,2))