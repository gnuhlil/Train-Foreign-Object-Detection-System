import cv2


# display lines over a image
def displayLines(image, lines):
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)  # converting to 1d array []
            # draw line over black image --(255,0,0) tells we want to draw blue line (b,g,r) values 10 is line thickness
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return image
