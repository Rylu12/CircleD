# import the necessary packages
import cv2
import math
import numpy as np

# now let's initialize the list of reference point

x_down =-1
y_down =-1
x_up =-1
y_up = -1
cropped_prev = []
b=0
cropped_line = [b]

def draw_line(event, x, y, flags, param):

    global x_down, y_down, x_up, y_up, cropped_prev, b, prev_cropped, cropped_line, factor, cropped

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    
    if event == cv2.EVENT_LBUTTONDOWN:
        x_down, y_down = x, y
        
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        x_up = x
        y_up = y

        cropped_prev.append(cropped.copy())  
        cv2.line(cropped, (x_up, y_up), (x_down,y_down), (0,255, 0), 2)
        length_line = (x_up-x_down)
        cropped_line.append(length_line)
        prev_cropped = np.array(cropped_prev)
        b = prev_cropped.shape[0]
    

# load the image, clone it, and setup the mouse callback function
def load_img(up_img):
    global cropped, factor, cropped_line
    image = cv2.imread(up_img, cv2.IMREAD_COLOR)
    orig = image.copy()

    height, width, rgb_value = image.shape

    #image = cv2.resize(image, (700, int(height/(width/700))), interpolation = cv2.INTER_AREA)

    #height, width, rgb_value = image.shape

    cropped = image[int(height*0.7):height, int(width*0.5):width]
    factor = 2
    resize_width = (width - int(width*0.5))*factor
    resize_height = (height - int(height*0.7))*factor

   # cv2.namedWindow("Cropped to measure scale-bar", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Cropped to measure scale-bar", int(resize_width), int(resize_height))
    cv2.imshow("Cropped to measure scale-bar", cropped)
    cv2.setMouseCallback("Cropped to measure scale-bar", draw_line)
    
# keep looping until the 'q' key is pressed to escape/end program
    
    
def drawLine():
    global b, cropped_line
    if b !=0:
        return cropped_line[b]
    else:
        return 1

