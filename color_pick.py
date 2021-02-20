import cv2
import numpy as np 

cap = cv2.VideoCapture(0)
cap.set(3,450)   #Changing width to 640
cap.set(4,450)   #Changing height to 480
cap.set(10,100)  #Changing brightness to 100

"""Creating trackbars to detect the HSV properties of the color we want to use"""

def empty():
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)

cv2.createTrackbar("Hue Min", "HSV", 0, 179, empty)
cv2.createTrackbar("Sat Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Val Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Hue Max", "HSV", 179, 179, empty)
cv2.createTrackbar("Sat Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Val Max", "HSV", 255, 255, empty)

"""Reading trackbar values"""

while True:

    _, img = cap.read()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "HSV")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV")
    v_min = cv2.getTrackbarPos("Val Min", "HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV")
    v_max = cv2.getTrackbarPos("Val Max", "HSV")
    print(h_min,s_min,v_min,h_max,s_max,v_max)

    """Creating a mask of the color we detected"""

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    img_mask = cv2.inRange(img_hsv, lower, upper)

    """Getting the colored mask using 'bitwise and' operator"""
    img_result = cv2.bitwise_and(img,img, mask= img_mask)

    cv2.imshow("Original", img)
    #cv2.imshow("HSV", img_hsv)
    cv2.imshow("Mask", img_mask)
    cv2.imshow("Result", img_result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
