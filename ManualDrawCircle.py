# import the necessary packages
import cv2
import math
import numpy as np

global currDiam, b
# now let's initialize the list of reference point
m_x = -1
m_y = -1
image_prev = []
image_diam = []

def draw_circle(event, x, y, flags, param):
    # grab references to the global variables
    global m_x, m_y, image_prev, b, prev_img, currDiam

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
        c_y = int((m_y+y)/2)
        rad = int(math.sqrt(((m_x-c_x)**2)+((m_y-c_y)**2)))
        
        #Copies the previous image before the last drawing, allows to delete later
        image_prev.append(image.copy())  
        cv2.circle(image, (c_x,c_y), rad , (0, 255, 0), 2)
        cv2.imshow("image", image)
        
      
        prev_img = np.array(image_prev)
        b = prev_img.shape[0]
        image_diam.append(rad*2)
        
        currDiam = image_diam[b]

def load_image(up_img):
# load the image, clone it, and setup the mouse callback function
    image = cv2.imread(up_img, cv2.IMREAD_COLOR)
    #orig = image.copy()

    h = int(image.shape[0]*0.5)     #rescale image to 50% size
    w = int(image.shape[1]*0.5)

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
            
        # if the 'q' key is pressed, break from the loop
        elif key == ord("q"):
            break
        

    # close all open windows
    cv2.destroyAllWindows() 