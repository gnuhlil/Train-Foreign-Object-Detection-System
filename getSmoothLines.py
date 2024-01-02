import cv2
import numpy as np
import getLineCoordinates as glc


# Avergaes all the left and right lines found for a lane and retuns single left and right line for the lane
def getSmoothLines(image, lines):
    left_fit = []  # will hold m,c parameters for left side lines
    right_fit = []  # will hold m,c parameters for right side lines

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # polyfit gives slope(m) and intercept(c) values from input points
        # last parameter 1 is for linear..so it will give linear parameters m,c
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = []
    right_fit_average = []
    flag = 0

    # take averages of all intercepts and slopes separately and get 1 single value for slope,intercept
    # axis=0 means vertically...see its always (row,column)...so row is always 0 position.
    # so axis 0 means over row(vertically)
    if flag == 0:
        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)

    # now we have got m,c parameters for left and right line, we need to know x1,y1 x2,y2 parameters
    left_line = glc.getLineCoordinates(image, left_fit_average)
    right_line = glc.getLineCoordinates(image, right_fit_average)
    return np.array([left_line, right_line])
