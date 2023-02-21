import cv2
import time
import numpy as np

# note
# telescope focal length: 360mm (f)
# camera: 19.1mm*13.0mm (h)
# pixel number: 4144*2822
# alpha = 2*np.arctan(h/2/f)
# FoV = 
# pixel size in arcsec: 2.64

def main(file_path):
    #path = 'satellite/data/Satllite_00055.tif'
    path = file_path
    img = cv2.imread(path,cv2.CV_8UC1)
    #img = cv2.imread('satellite/data/Satllite_00055.tif')
    #cv2.imshow('image', img)

    kernel1 = np.ones((3, 3)) / 5

    avg_filtered = cv2.filter2D(img, -1, kernel1)

    #cv2.imshow('Average filtered', avg_filtered)

    ret, binary = cv2.threshold(avg_filtered, 205, 255, cv2.THRESH_BINARY)
    #cv2.imshow('binary', binary)

    #erode1
    kernel2 = np.ones((3,3), np.uint8)
    erode1 = cv2.erode(binary, kernel2, iterations = 1)
    #cv2.imshow('erode1',erode1)

    #erode2
    kernel2_5 = np.ones((2,2), np.uint8)
    erode2 = cv2.erode(erode1, kernel2_5, iterations = 1)
    #cv2.imshow('erode2',erode2)

    #dilation
    kernel3 = np.ones((3,3), np.uint8)
    dilation = cv2.dilate(erode2, kernel3, iterations = 2)
    #cv2.imshow('dilation',dilation)

    # contour
    contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # other image
    img_plot = cv2.imread(path)
    #print(np.shape(img_plot))

    # report contour position from the mask
    def report_mask_posit(img, cnt):
        posit = np.mean(cnt, axis=0)[0]
        x, y = posit
        x = int(x)
        y = int(y)
        print_posit = "(" + str(x) + ", " + str(y) + ")"
        #print('position: ', "{:<4d}".format(x), "{:<4d}".format(y))
        cv2.putText(img, print_posit, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50,170,50), 1)
        return
    
    # calculate contour position from origin image
    def report_cont_posit(img, cnt, cnt_num):
        cont_inf = np.array([[i[0], i[1], np.max(img[i[0]][i[1]])] \
                            for i in np.flip(np.reshape(cnt, (np.shape(cnt)[0], 2)))])
        T_cont_inf = np.transpose(cont_inf)
        x = np.sum(T_cont_inf[0]*T_cont_inf[2]) / np.sum(T_cont_inf[2])
        y = np.sum(T_cont_inf[1]*T_cont_inf[2]) / np.sum(T_cont_inf[2])
        x = int(x)
        y = int(y)
        print_posit = str(cnt_num) + ": (" + str(y) + ", " + str(x) + ")"
        cv2.putText(img, print_posit, (y-10, x-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        return 

    # draw contour
    cnt_num = 0
    for cnt in contours:
        #record contour's order
        cnt_num += 1

        # count object's contour size
        area = cv2.contourArea(cnt)

        # set box around object
        x, y, w, h = cv2.boundingRect(cnt)

        # draw contours around the object
        #cv2.drawContours(img_plot, [cnt], -1, (0, 255, 0), 1)
        # draw box around the object
        #cv2.rectangle(img_plot, (x,y), (x + w, y + h), (0, 255, 0), 1)

        # draw contours and box based on certain area 
        #if area > np.min(area):
            #cv2.drawContours(img_plot, [cnt], -1, (0, 255, 0), 2)
            #x, y, w, h = cv2.boundingRect(cnt)
            #cv2.rectangle(img, (x,y), (x + w, y + h), (0, 255, 0), 3)
            #print(x, y, w, h)
        
        # report the position from the mask
        #report_mask_posit(img_plot, cnt)
        report_cont_posit(img_plot, cnt, cnt_num)
    
    #window size and place
    cv2.namedWindow('image')
    cv2.moveWindow('image', 300, 300)
    cv2.imshow('image', img_plot)
   #print(cnt_num)

    k = cv2.waitKey(500)
    #time.sleep(1)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    switch = "on"

    if switch == "off":
        main('satellite/data/Satllite_00003.tif')
    else:
        for i in range(100):
            i = i+1
            if i < 10:
                the_path = "satellite/data/Satllite_0000"+str(i)+".tif"
                #print(the_path)
                #img = cv2.imread(the_path)
                #video.write(img)
                main(the_path)
            if (i>=10) and (i < 100):
                the_path = "satellite/data/Satllite_000"+str(i)+".tif"
                #print(the_path)
                #img = cv2.imread(the_path)
                #video.write(img)
                main(the_path)
            if (i>=100) and (i < 999):
                the_path = "satellite/data/Satllite_00"+str(i)+".tif"
                #print(the_path)
                #img = cv2.imread(the_path)
                #video.write(img)
                main(the_path)
        cv2.destroyAllWindows()

'''
#cap = cv2.VideoCapture('satellite/data/Satllite_00001.tif')
cap = cv2.VideoCapture('satellite/sate_track_2.avi')

# Mask
object_detector = cv2.createBackgroundSubtractorMOG2(history=3, varThreshold=10)

play=1

while cap.isOpened():
    if (play):
        ret, frame = cap.read()
        #cv2.imshow('frame', frame)

        roi = frame[350:650, 800:1100]
        cv2.imshow('roi', roi)

        #mask = object_detector.apply(roi)
        #cv2.imshow('mask', mask)

        #erode
        kernel = np.ones((3,3), np.uint8)
        dilate = cv2.dilate(roi, kernel, iterations = 1)
        cv2.imshow('dilate',dilate)

        mask = object_detector.apply(dilate)
        cv2.imshow('mask', mask)

        time.sleep(1)

    key = cv2.waitKey(24)
    # Enter:13, Esc:27, Up:82, Down:84, Left:81, Right:83
    if key == 27:
        break
    elif key == 32:
        play = play ^ 1

'''