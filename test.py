import cv2
import time
#from tracker import *

#cap = cv2.VideoCapture('satellite/sate_track_1.avi')
cap = cv2.VideoCapture(0)

# Mask
object_detector = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=50)
#object_detector = cv2.createBackgroundSubtractorKNN(history=30, dist2Threshold=50)

play = 1
while cap.isOpened():
    if (play):
        # import video
        ret, frame = cap.read()
        #rotated=cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        #height, width, _ = frame.shape
        #print(height, width)

        # Extract Region of interest
        #roi = frame[300:700, 760:1160]
        #[1920:1080]
        roi = frame
        #roi = frame[200:800, 460:1460]
        #roi = frame[460:1460, 200:800]
        #roi = frame[350:650, 800:1100]
        #roi = frame[500:900, 700:1600]

        # Start timer
        timer = cv2.getTickCount()

        # Object Detection
        #mask = object_detector.apply(frame)
        mask = object_detector.apply(roi)
        _, mask = cv2. threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            print(cnt.shape)
            area = cv2.contourArea(cnt)
            if area > 5:
                #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(roi, (x,y), (x + w, y + h), (0, 255, 0), 3)
                print(x, y, w, h)


        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # Display FPS on frame
        cv2.putText(roi, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        cv2.imshow('roi', roi)
        #cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)

        time.sleep(0.1)
    
    
    key = cv2.waitKey(24)
    # Enter:13, Esc:27, Up:82, Down:84, Left:81, Right:83
    if key == 27:
        break
    elif key == 32:
        play = play ^ 1

