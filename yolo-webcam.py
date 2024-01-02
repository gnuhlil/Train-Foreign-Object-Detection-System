import cv2
import numpy as np
import canny
import getROI
import getLines
import getSmoothLines as getSL
import alert
import displayLines as display
import winsound

# Load Yolo
net = cv2.dnn.readNet(
    r"C:\Users\ASUS\Desktop\project\yolo_weight\yolov4-tiny.weights",
    r"C:\Users\ASUS\Desktop\project\yolo_cfg\yolov4-tiny.cfg",
)
classes = []
with open(r"C:\Users\ASUS\Desktop\project\yolo-coco\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

flag = 1  # 1:依據鐵軌直線判斷異物是否入侵  2:依據ROI是否有東西判斷是否入侵

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# cap = cv2.VideoCapture(0)
videoFeed = cv2.VideoCapture(
    r"C:\Users\ASUS\Desktop\project_2\videos\warningSystem_test.mp4"
)
if not videoFeed.isOpened():
    print("Cannot read video")
    exit()
while videoFeed.isOpened():
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    ret, frame = videoFeed.read()
    height, width, channels = frame.shape
    image = frame

    edged_image = canny.cannyEdgeDetector(image)  # Step 1
    roi_image = getROI.getROI(edged_image)  # Step 2
    lines = getLines.getLines(roi_image)  # Step 3
    smooth_lines = getSL.getSmoothLines(image, lines)  # Step 4

    # Detecting objects
    if flag == 1:
        blob = cv2.dnn.blobFromImage(
            frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
        )
    if flag == 2:
        roi_image = getROI.getROI(frame)
        blob = cv2.dnn.blobFromImage(
            roi_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False
        )

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(indexes) != 0:
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                cv2.putText(frame, label, (x, y - 20), font, 0.7, color, 1)

    if flag == 1:
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                alert.alert(x, y, w, h, smooth_lines)
    if flag == 2:
        if len(indexes) != 0:
            winsound.Beep(2222, 111)  # 主板蜂鸣器
            winsound.MessageBeep()  # 喇叭

    frame = display.displayLines(frame, smooth_lines)  # Step 5

    cv2.putText(
        frame,
        "FPS: {0:.2f}".format(frame_rate_calc),
        (30, 50),
        font,
        0.7,
        (255, 255, 0),
        1,
    )
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", 960, 540)
    cv2.imshow("Image", frame)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # Press 'q' to quit
    if cv2.waitKey(1) == ord("q"):
        break

videoFeed.release()
cv2.destroyAllWindows()
