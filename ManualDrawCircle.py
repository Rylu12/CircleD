# import the necessary packages
import cv2
import math
import numpy as np

# now let's initialize the list of reference point
m_x = -1
m_y = -1
b = 0
image_prev = []
image_diam = [0]

def draw_circle(event, x, y, flags, param):
    # grab references to the global variables
    global m_x, m_y, image_prev, prev_img, currDiam, image, ratio, b

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
        try:  
            image_prev.append(image.copy())  
            cv2.circle(image, (c_x,c_y), rad , (0, 255, 0), 2)

            prev_img = np.array(image_prev)
           
            b = prev_img.shape[0]
            image_diam.append(np.round((rad*2/ratio),1))
        except MemoryError:
            cv2.destroyAllWindows()

def load_img(up_img, pixel_dist):
    global image, image_prev, prev_img, ratio
# load the image, clone it, and setup the mouse callback function
    image = cv2.imread(up_img, cv2.IMREAD_COLOR)

    ratio = pixel_dist

    img_height, img_width, rgb_value = image.shape

    max_wh = max(img_width, img_height)
    if max_wh > 800:
        factor = max_wh / 800
    elif max_wh > 600 and max_wh < 800:
        factor = max_wh
    else:
        factor = max_wh/800
    

    cv2.resizeWindow('Manual Draw Mode', int(img_width / factor), int(img_height / factor))
    cv2.imshow('Manual Draw Mode', image)
    cv2.setMouseCallback('Manual Draw Mode', draw_circle)
  
def diamCircles(state):
    global image_diam, image_diam, image_prev, b
    
    if state == False:
        image_diam.pop()
        image_prev.pop()
        b = b-1
    elif b == (len(image_diam)-1):
        return image_diam[b]


