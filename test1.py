import cv2
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

# read video
#video = cv2.VideoCapture('satellite/sate_track_1.avi')
video = cv2.VideoCapture(0)

# set tracker
tracker_type='Boosting'

tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerGOTURN_create() #broken
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCSRT_create()


# read first frame
ok, frame = video.read()
height, width, _ = frame.shape
#print(height, width)
ratio_x = 0.15
ratio_y = 0.15

roi = frame[int(height*ratio_y):int(height*(1-ratio_y)), int(width*ratio_x):int(width*(1-ratio_x))]

# define the initial bounding box
#bbox = (287, 23, 86, 320)
bbox = cv2.selectROI(roi, False)
ok = tracker.init(roi, bbox)
#print(bbox)

plt.ion()

init_bbox = [int(bbox[0]), int(bbox[1])]
times_cont = 0
while True:
    # times cont
    times_cont += 1
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break
    roi = frame[int(height*ratio_y):int(height*(1-ratio_y)), int(width*ratio_x):int(width*(1-ratio_x))]

    # Start timer
    timer = cv2.getTickCount()
 
    # Update tracker
    ok, bbox = tracker.update(roi)
 
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(roi, p1, p2, (255,0,0), 2, 1)
        #print(p1)
    else :
        # Tracking failure
        cv2.putText(roi, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
    # Display tracker type on frame
    cv2.putText(roi, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),1)

    # Display the frame order
    cv2.putText(roi, str(times_cont) + "frames", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),1)
     
    # Display FPS on frame
    #cv2.putText(roi, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
 
    # Display result
    cv2.namedWindow('Tracking')
    cv2.moveWindow('Tracking', 250, 80)
    cv2.imshow("Tracking", roi)

    posit = np.array([p1[0]+bbox[2]/2, p1[1]+bbox[3]/2])

    # plot
    '''
    plt.scatter(posit[0], posit[1], alpha=0.3, c='k')
    if times_cont == 1:
        init_bbox[0] = int(bbox[0]+bbox[2]/2)
        init_bbox[1] = int(bbox[1]+bbox[3]/2)
    plt.xlim(init_bbox[0]-20, init_bbox[0]+20)
    plt.ylim(init_bbox[1]-20, init_bbox[1]+20)
    plt.title("satellite's drift")
    plot_tic = np.array([-20, -15, -10, -5, 0, 5, 10, 15, 20])
    numb_x = np.array([init_bbox[0]-20, init_bbox[0]-15, init_bbox[0]-10, init_bbox[0]-5, init_bbox[0],\
                       init_bbox[0]+5, init_bbox[0]+10, init_bbox[0]+15, init_bbox[0]+20])
    numb_y = np.array([init_bbox[1]-20, init_bbox[1]-15, init_bbox[1]-10, init_bbox[1]-5, init_bbox[1],\
                       init_bbox[1]+5, init_bbox[1]+10, init_bbox[1]+15, init_bbox[1]+20])
    plot_tic = np.round(plot_tic * 2.64, 2)
    plot_tic = [str(i) for i in plot_tic]
    plt.xticks(numb_x, plot_tic)
    plt.yticks(numb_y, plot_tic)
    plt.xlabel(r'$\Delta$ x (in pic frame)[arcsec]')
    plt.ylabel(r'$\Delta$ y (in pic frame)[arcsec]')
    
    plt.draw()
    '''

    # some delay
    #time.sleep(1)

 
    # Exit if ESC pressed
    k = cv2.waitKey(1)
    if k == 27 : break

'''
play = 1
while cap.isOpened():
    if (play):
        # import video
        ret, frame = cap.read()
        #h, w, _ = frame.shape
        #print(h, w)
        rotated=cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        h1, w1, _ = rotated.shape
        roi = rotated[600:1300, 200:800]
        cv2.imshow('roi', roi)

    key = cv2.waitKey(24)
    # Enter:13, Up:82, Down:84, Left:81, Right:83
    if key == 13: #Esc
        break
    elif key == 32: #space
        play = play ^ 1


cap.release()
cv2.destroyAllWindows()
'''
