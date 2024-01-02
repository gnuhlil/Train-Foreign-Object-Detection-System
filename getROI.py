import cv2
import numpy as np


def getROI(image):
    height = image.shape[0]
    width = image.shape[1]

    # Defining Triangular ROI: The values will change as per your camera mounts
    triangle = np.array(
        [[(760, height), (460, height), (620, 320)]]
    )  # warningSystem_test.mp4
    # triangle = np.array([[(1050, height), (280, height), (550, 250)]])  # road.mp4
    # triangle = np.array([[(600, height), (1200, height), (970, 470)]])  # rail.mp4

    # creating black image same as that of input image
    black_image = np.zeros_like(image)
    # Put the Triangular shape on top of our Black image to create a mask
    mask = cv2.fillPoly(black_image, triangle, (255, 255, 255))
    # applying mask on original image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
