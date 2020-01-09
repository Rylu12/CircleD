import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

#Get pixel/distance (using ImageJ software) to output actual diameters of circles
global result, img

def autoDetect(up_img):
    global result, img
    distance = 1
    pixel = 1.012
    pixel_distance = pixel/distance

    # Read image.
    img = cv2.imread(up_img, cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    accum_ratio = 1
    min_dist = 20
    p1 = 30
    p2 = 30
    minR = 1
    maxR = 50

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, dp = accum_ratio, minDist = min_dist, 
                       param1 = p1, param2 = p2, minRadius = minR, maxRadius = maxR)

    # Draw circles that are detected.
    if detected_circles is not None:
        
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            
        

        cv2.imwrite(up_img.replace('.jpg', '_detected.jpg'),img)
        print(detected_circles)
        print()
        rad_list=[]
        
        #Loop to convert radius (pixel) values to diameter
        for x in range(detected_circles.shape[1]):
            diam = detected_circles[0,x,2]*2/pixel_distance    
            rad_list.append(round(diam,1))

        print(type(round(diam,1)))
        print(rad_list.sort())
        print(rad_list)
        print()
        output_list = []
        bottom_10percentile = int(len(rad_list)*0.1)
        top_90percentile = int(len(rad_list)*0.9)

        result = 'Number of circles found: ' + str(detected_circles.shape[1]) 
        result +='\nAverage diameter of circles = ' + "%.1f"%np.average(rad_list) + 'um' 
        result +='\nD10 = '+ str(rad_list[bottom_10percentile])+'um'+'\nD50 = ' + "%.1f"%np.median(rad_list) + "um" 
        result +='\nD90 = '+ str(rad_list[top_90percentile])+'um'

        #Plot histogram
        plt.xlabel('Diameter (um)')
        plt.ylabel('Frequency')
        plt.title('Particle Size Distribution')
        (n, bins, patch) = plt.hist([rad_list], bins=np.arange(0,101,10), rwidth=0.9)
        plt.xticks(np.arange(0,101,10))
      #  plt.gca().grid(which='major', axis='y')
        plt.savefig(up_img.replace('.jpg', '_histogram.png'), dpi = 500)
        
        

        print('# of count in each bin = \n', n)
        print('Bins range = \n', np.ndarray.round(bins))

        rad_list.append(p1)
        rad_list.append(p2)
        rad_list.append(minR)
        rad_list.append(maxR)

        pd.DataFrame(rad_list).to_excel('emulsions_D50_list_1.xlsx',header=False, index=False)


def clear_plt():
    plt.clf()