import cv2
import numpy as np


def getLines(image):
    # lines=cv2.HoughLinesP(image,bin_size,precision,threshold,dummy 2d array--no use,minLineLength,maxLineGap)
    # lets take bin size to be 2 pixels
    # lets take precision to be 1 degree= pi/180 radians
    # threshold is the votes that a bin should have to be accepted to draw a line
    # minLineLength --the minimum length in pixels a line should have to be accepted.
    # maxLineGap --the max gap between 2 broken line which we allow for 2 lines to be connected together.

    lines = cv2.HoughLinesP(image, 1, np.pi / 180, 100, minLineLength=5, maxLineGap=30)
    return lines
