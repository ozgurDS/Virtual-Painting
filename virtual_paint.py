import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,450)   #Changing width to 640
cap.set(4,450)   #Changing height to 480
cap.set(10,150)  #Changing brightness to 100

"""To detect the HSV values of the colors we will use for drawing, 
   we used another code file we created for this project named color_pick. 
   Order of the HSV parameters in my_colors:[h_min, s_min, v_min, h_max, s_max, v_max]"""

my_colors = [[92, 147, 112, 115, 255, 255],
             [67, 55, 35, 85, 235, 202],
             [161, 155, 82, 179, 255, 235]]

my_color_values = [[255,255,0],
                   [0,255,0],
                   [0,0, 230]]
                
my_points = []   ##[x, y, colorIndex]

"""Defining the function that determines the color of the virtual pen and 
   mark the tip of the pen which we will use to draw virtual paints"""

def findColor(img_in, my_colors, my_color_values):
    img_hsv = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV)
    counter = 0
    new_points = []
    for color in my_colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        img_mask = cv2.inRange(img_hsv, lower, upper)
        x,y = getContours(img_mask)
        cv2.circle(img_result,(x,y), 10, my_color_values[counter], cv2.FILLED)
        if x!=0 and y!=0:
            new_points.append([x,y,counter])
        counter +=1
        #cv2.imshow(str(color[0]), img_mask)
    return new_points

"""Defining the function that gets the contour area properties of the virtual pen"""

def getContours(img_in):
    contours, hierarcy = cv2.findContours(img_in, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0   ##In case there is no available contour, function will return these values
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >10:   ##Adding a logical threshold prevents detection of some small noices
         #cv2.drawContours(img_result, cnt, -1, (255,255,255),2)
         par = cv2.arcLength(cnt, True)
         approx = cv2.approxPolyDP(cnt, 0.02*par, True)  ##The corner points for each contour
         x,y,w,h = cv2.boundingRect(approx) 
    return x+w//2,y   ##This will give the tip point of the virtual pen

"""Defining the function that draws on the screen"""

def drawOnScreen(my_points, my_color_values):
    for point in my_points: 
        cv2.circle(img_result,(point[0], point[1]), 10, my_color_values[point[2]], cv2.FILLED)

"""Below is the cell that executes the program"""

while True:
    success, frame = cap.read()
    img_result = frame.copy()
    new_points = findColor(frame, my_colors, my_color_values)
    
    if len(new_points)!=0:
        for new_point in new_points:
            my_points.append(new_point)
    if len(my_points)!=0:
        drawOnScreen(my_points,my_color_values)

    cv2.imshow("Result", img_result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()