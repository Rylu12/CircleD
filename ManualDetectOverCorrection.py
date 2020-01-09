# import the necessary packages
import cv2
import math
import numpy as np
 
# now let's initialize the list of reference point
global m_x, m_y
m_x = -1
m_y = -1
image_prev =[]
 
def draw_circle(event, x, y, flags, param):
    # grab references to the global variables
    global m_x, m_y, image_prev, b, prev_img
   
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
   
    if event == cv2.EVENT_LBUTTONDOWN:
        m_x, m_y = x, y
       
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
       
        # draw a circle around the object (pt1 to pt2 is the diameter)
        c_x = int((m_x+x)/2)
        print('mx =' + str(m_x) + ', x =' + str(x))
        c_y = int((m_y+y)/2)
        print('my =' +str(m_y) + ', y =' + str(y))
        rad = int(math.sqrt(((m_x-c_x)**2)+((m_y-c_y)**2)))
        diam = rad*2
 
        #Copies the previous image before the last drawing, allows to delete later
        image_prev.append(image.copy()) 
        
        
        cv2.imshow("image", image)
       
      
        prev_img = np.array(image_prev)
        b = prev_img.shape[0]
        print("Diam = " + str(diam) + ', c_x = ' +str(c_x) + ', c_y = ' +str(c_y))
 
        y1= int(c_y-rad*2)
        y2 = int(c_y+rad*2)
        x1= int(c_x-rad*2)
        x2 = int(c_x+rad*2)
 
        if y1 and y2 and x1 and x2 != 0:
       
            cropped = image[y1:y2, x1:x2].copy()
            cv2.imshow("Cropped", cropped)
            print(y1, y2, x1, x2)
            #Convert to grayscale.
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            # Blur using 5 * 5 kernel.
            gray_blurred = cv2.blur(gray, (5, 5))
      
            detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 100, param1 = 50,
                          param2 = 50, minRadius = int(rad*0.75), maxRadius = int(rad*1.25))
           
            if detected_circles is not None:
                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
          
                # Draw the circumference of the circle.
                cv2.circle(image, (a, b), r, (0, 255, 255), 2)
                cv2.circle(cropped, (a, b), r, (0, 255, 255), 2)
 
                print('Drawn x,y = ' + str(a) + ' '+ str(b))
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
        else:
            cv2.circle(image, (c_x,c_y), rad , (0, 255, 0), 2)
        cv2.imshow("cropped", cropped)        
# load the image, clone it, and setup the mouse callback function
image = cv2.imread('emulsions_B4C_100um_5.tif', cv2.IMREAD_COLOR)
 
orig = image.copy()
 
h = int(image.shape[0]*0.6)     #rescale image to 60% size
w = int(image.shape[1]*0.6)
 
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", w,h)
cv2.setMouseCallback("image", draw_circle)
 
# keep looping until the 'q' key is pressed to escape/end program
 
while True:
    # display the image and wait for a keypress
   
    cv2.imshow("image", image)
   
    key = cv2.waitKey(1) & 0xFF
 
    # press 'r' to reset the window
    if key == ord("r"):
        image = orig.copy()
       
    elif key == ord("d"):
        b = b-1
        image = prev_img[b]
        image_prev.pop
        print("Circle deleted")
       
    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break
   
 
# close all open windows
cv2.destroyAllWindows()

