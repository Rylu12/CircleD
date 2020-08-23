import tkinter as tk
from PIL import ImageTk, Image
import tkinter.scrolledtext as tkst
from tkinter import filedialog
import AutoDetectCircle as adc
import cv2
import matplotlib.pyplot as plt
import tkintertable as tkt
import numpy as np
import ManualDrawLine as mdl
import ManualDrawCircle as mdc

#Initialize GUI with root and set window dimensions
root = tk.Tk()
root.title("CirlceD - The Circle Detection Program")
root.geometry('1055x625')
root.tk.call('tk', 'scaling', 1.2)

 
#Initialize parameters
reset = False
calibrated = False

#Initialize tkintertable dictionary set up
table_Data = {'rec1': {'Col1': 'Diam.', 'Col2': 'values', 'Col3': 'will'}, 'rec2':{'Col1': 'go', 'Col2': 'here', 'Col3': ' '}, 
                'rec3': {'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 'rec4':{'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 
                'rec5':{'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 'rec6': {'Col1': ' ', 'Col2': ' ', 'Col3': ' '}}

#Initialize output display
output = 'Output results will display below...\n----------------------\n'
start_state = False


#Initialize window logo and logo frame
logo_img = ImageTk.PhotoImage(Image.open('circleD_V.png'))
logo_show = tk.Label(root, image=logo_img)
logo_show.grid(row =0, column = 0, rowspan = 15)


#Initialize intro text frame
frame_intro = tk.LabelFrame(root, width=80)
frame_intro.grid(row=0, column=1, rowspan=15, columnspan=5, pady=10, sticky = 'w')
 
intro_text = tkst.ScrolledText(frame_intro, wrap=tk.WORD, width=60, height=13, undo=False)
intro_text['font'] = ('consolas', '10')
intro_text.insert(tk.INSERT,
                  "Welcome to the Spherical Detection program!\n\nThis software program uses the 'Circle Hough Transform' (CHT) feature extraction technique to detect circles in images. "
                  "Circle candidates are produced by 'voting' in the Hough parameter space and selecting the local maxima in the accumulator matrix. "
                  "Hence, not all circles may be detected and the parameters have to be optimized to prevent over-detection/under-detection of circles."
                  "\n-----------------------------------------------"
                  "\nManual circle detection is also an option. Simply 'click and drag' from one side of a circle to the other side in the pop-up image window."
                  "\n\nReadings:\nhttps://en.wikipedia.org/wiki/Circle_Hough_Transform\n\nDescription of Hough Circle parameters:\nhttps://docs.opencv.org/3.4/d3/de5/tutorial_js_houghcircles.html")
 
intro_text.pack(expand=True, fill='both')


#Initialize all other frames in GUI
frame_output = tk.LabelFrame(root, bg='BLACK')
frame_output.grid(row=0, column=8, rowspan=55, columnspan=2, padx=10, pady=10, sticky='n')
 
output_text = tkst.ScrolledText(frame_output, wrap=tk.WORD, width=30, height=27, undo=False)
output_text['font'] = ('consolas', '11')
output_text.insert(tk.INSERT, str(output))
output_text.pack(expand=True, anchor='n')

frame_rdbutton = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_rdbutton.grid(row=15, column=0, rowspan=10, columnspan=5, padx=10, pady=5, sticky='w')
frame_start = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_start.grid(row=15, column=5, rowspan=10, padx=0, pady=5)
frame_upload = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_upload.grid(row=25, rowspan=10, column=5, columnspan=1, padx=0, pady=5, sticky = 's')
 
frame_preview = tk.LabelFrame(root)
frame_preview.grid(row=35, column=4, rowspan=35, columnspan=2, padx=5, pady=5, sticky = 'nw')

frame_binary = tk.LabelFrame(root, text = "Binary Filter Mode")
frame_binary.grid(row=56, column=8, rowspan = 13, columnspan=3, padx=10, pady=5, sticky = 'w')

frame_histo_show = tk.LabelFrame(root)
frame_histo_show.grid(row=40, column = 0, rowspan = 32, columnspan = 4, padx=10, pady=3, sticky = 'nw')

frame_table = tk.LabelFrame(root)
frame_table.grid(row = 0, column = 10,  rowspan = 45, columnspan = 2, padx=5, pady=9, sticky = 'n')


table_label = tk.Label(root, text ='To Export Table Above:\n------\nRight-Click -> File -> Export CSV', font=("Helvetica", 9))
table_label.grid(row = 56, rowspan = 10, column = 10, columnspan = 2)

histo_img = Image.open('histo244x183.png')
smaller_histo_img = ImageTk.PhotoImage(histo_img)
new_img_histo = tk.Label(frame_histo_show,image = smaller_histo_img)
new_img_histo.pack()

 
frame_HoughCircle = tk.LabelFrame(root, text='Hough Circle Parameters', width=70, padx=10, pady=5)
frame_HoughCircle.grid(row=25, column=0, rowspan = 10, columnspan=5, padx=10, pady=5, sticky='w')
 
param_minDist = tk.Entry(frame_HoughCircle, width=4)
param_minDist.insert(0, str(adc.min_dist))
param_minDist.grid(row=0, column=1, padx=1, pady=1)
label_minDist = tk.Label(frame_HoughCircle, text='Min Distance (um):')
label_minDist.grid(row=0, column=0, padx=1, pady=1)
 
param_dp = tk.Entry(frame_HoughCircle, width=4)
param_dp.insert(0, str(adc.accum_ratio))
param_dp.grid(row=1, column=1, padx=1, pady=1)
label_dp = tk.Label(frame_HoughCircle, text='Accum/Res Ratio (dp):')
label_dp.grid(row=1, column=0, padx=1, pady=1)
 
param_minDiam = tk.Entry(frame_HoughCircle, width=4)
param_minDiam.insert(0, str(adc.minDiam))
param_minDiam.grid(row=0, column=3, padx=1, pady=1)
label_minDiam = tk.Label(frame_HoughCircle, text=' Min Diam (um):')
label_minDiam.grid(row=0, column=2, padx=1, pady=1)
 
param_maxDiam = tk.Entry(frame_HoughCircle, width=4)
param_maxDiam.insert(0, str(adc.maxDiam))
param_maxDiam.grid(row=1, column=3, padx=1, pady=1)
label_maxDiam = tk.Label(frame_HoughCircle, text=' Max Diam (um):')
label_maxDiam.grid(row=1, column=2, padx=1, pady=1)
 
param_p1 = tk.Entry(frame_HoughCircle, width=4)
param_p1.insert(0, str(adc.p1))
param_p1.grid(row=0, column=5, padx=1, pady=1)
label_p1 = tk.Label(frame_HoughCircle, text=' Param1:')
label_p1.grid(row=0, column=4, padx=1, pady=1)
 
param_p2 = tk.Entry(frame_HoughCircle, width=4)
param_p2.insert(0, str(adc.p2))
param_p2.grid(row=1, column=5, padx=1, pady=1)
label_p2 = tk.Label(frame_HoughCircle, text=' Param2:')
label_p2.grid(row=1, column=4, padx=1, pady=1)


frame_histo_param = tk.LabelFrame(root, text='Histogram Parameters', padx=10, pady=5)
frame_histo_param.grid(row=35, column=0, rowspan = 5, columnspan=4, padx=10, pady=5, sticky = 'w')
 
interval_bins = tk.Entry(frame_histo_param, width=4)
interval_bins.insert(0, str(adc.intervals))
interval_bins.grid(row=0, column=1, padx=1)
label_bins = tk.Label(frame_histo_param, text='Intervals')
label_bins.grid(row=0, column=0, padx=1)
 
minRange = tk.Entry(frame_histo_param, width=4)
minRange.insert(0, str(adc.min_range))
minRange.grid(row=0, column=3, padx=1)
label_minRange = tk.Label(frame_histo_param, text='Min\nRange ')
label_minRange.grid(row=0, column=2, padx=1)

maxRange = tk.Entry(frame_histo_param, width=4)
maxRange.insert(0, str(adc.max_range))
maxRange.grid(row=0, column=5, padx=1)
label_maxRange = tk.Label(frame_histo_param, text='Max\nRange ')
label_maxRange.grid(row=0, column=4, padx=1)


frame_scalebar = tk.LabelFrame(root, text = "Calibrates Pixel/Distance Ratio", padx=5, pady=5)
frame_scalebar.grid(row=44, column=8,  rowspan = 12, columnspan=3, padx=10, pady=5, sticky='nw')

scalebar = tk.Entry(frame_scalebar, width=7)
scalebar.insert(0, str(adc.scalebar))
scalebar.grid(row=2, column=4, columnspan = 2, padx=1, pady=1, sticky = 'w')
label_scalebar = tk.Label(frame_scalebar, text='Known distance of scale-bar (um):')
label_scalebar.grid(row=2, column=0, columnspan = 4, padx=1, pady=1)

pixel_dist = tk.Entry(frame_scalebar, width=6, state = 'readonly')
pixel_dist.grid(row=3, column=1, padx=1, pady=1, sticky = 'w')
label_pixel_dist = tk.Label(frame_scalebar, text='Pixel/Distance Ratio:')
label_pixel_dist.grid(row=3, column=0, padx=1, pady=1, sticky = 'w')

frame_sbLocation = tk.LabelFrame(root, text ='Scale-Bar Location?', padx = 5, pady = 5)
frame_sbLocation.grid(row = 44, column = 11, rowspan = 13, padx = 5, pady=7, sticky = 'nw')

#Initialize radiobutton functions for scale calibration
sb_text = tk.StringVar()
sb_location = 'br'
sb_text.set('br')
 
tk.Radiobutton(frame_sbLocation, text="Top-Left",
               variable=sb_text, value='tl', command=lambda: sbLocation_clicked('tl')).grid(row = 0, column = 0, sticky = 'w')
tk.Radiobutton(frame_sbLocation, text="Top-Right",
               variable=sb_text, value='tr', command=lambda: sbLocation_clicked('tr')).grid(row = 0, column = 1, sticky = 'w')
tk.Radiobutton(frame_sbLocation, text="Bottom-Left",
               variable=sb_text, value='bl', command=lambda: sbLocation_clicked('bl')).grid(row = 1, column = 0, sticky = 'w')
tk.Radiobutton(frame_sbLocation, text="Bottom-Right",
               variable=sb_text, value='br', command=lambda: sbLocation_clicked('br')).grid(row = 1, column = 1, sticky = 'w')


def sbLocation_clicked(value):
    global sb_location
    if value == 'tl':
        sb_location = value
    elif value == 'tr':
        sb_location = value
    elif value == 'bl':
        sb_location = value
    elif value == 'br':
        sb_location = value

#Initialize image display as default black image
black_img = Image.open('black250.png')
black_img = black_img.resize((250,250))
temp_img = ImageTk.PhotoImage(black_img)
placeholder_img = tk.Label(frame_preview, image=temp_img).pack()
 

table = tkt.TableCanvas(frame_table, data = table_Data,
            cellwidth=30, cellbackgr='white',
            thefont=('Arial',10), width = 182, height = 384,
            rowselectedcolor='#f8eba2')
table.show()
 
yesNoState = tk.StringVar()
yesNoState.set('NO')
binState = 'NO'
filename_copy = ''


def open_file():
    """
    Function to upload and open image files
    """

    global open_img, window_img, placeholder_img, show_img, img_width, img_height, filename
    global max_wh, adj_height, binary_state, resized_img_cv2, resize_img, calibrated, filename_copy

    black_img = Image.open('black250.png')
    temp_img = ImageTk.PhotoImage(black_img)
    placeholder_img = tk.Label(frame_preview, image=temp_img, bg ='black').place(x=0, y=0)
 
    filename = filedialog.askopenfilename(initialdir='C:\\', title="Select a file",
                                          filetypes=(
                                          ("jpg Files", "*jpg"), ("png Files", "*png"), ("tif Files", "*tif")))

    if (filename != (filename_copy[:-4] + '_detected' + filename_copy[-4:])):
        calibrated = False
    else:
        calibrated = True

    resize = False
    if filename:
        try:  
            open_img = Image.open(filename).convert("RGB")
        except IOError: 
            return
     
        img_width, img_height = open_img.size
        
        max_wh = max(img_width, img_height)

        resize_copy = max_wh/800
        resize_img = open_img.resize((int(img_width/resize_copy), int(img_height/resize_copy)))
        resized_img_cv2 = np.asarray(resize_img)  

        factor = max_wh/250

        open_img = open_img.resize((int(img_width / factor), int(img_height / factor)))

        adj_height = (250 - (img_height / factor)) / 2

        window_img = ImageTk.PhotoImage(open_img)
        show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
        binary_state.config(state = 'normal')


def start_state():
    """
    Function to start auto detection or manual detection mode after uploading file
    """

    global filename, temp_img, detected_img, output, smaller_histo_img, ratio, reset, binState, pixel_dist
    global new_img_histo, img_width, img_height, bin_img, table_Data, table, binary_thresholdBar
    global resized_img_cv2, max_wh, calibrated, output_text, filename_copy

    try:
        open_img_again = Image.open(filename).convert("RGB")
        max_wh = max(img_width, img_height)
        resize_copy = max_wh/800
        resize_img = open_img_again.resize((int(img_width/resize_copy), int(img_height/resize_copy)))
        resized_img_cv2 = np.asarray(resize_img)  

    except (NameError, AttributeError) as e:
        output_text.insert(tk.INSERT, '\n\nERROR...Please upload an image before running!\n\n')

        filename = None

    if filename != None:

        filename_copy = filename

        if calibrated != True:
            output_text.insert(tk.INSERT, '\n\nERROR...Please calibrate image before running!\n\n')
            return
        if filename:
            pixel_dist.configure(state='normal')
            pixel_dist.delete(0, 'end')
            input_scale = float(str(scalebar.get()))
  
            ratio = np.round(abs(mdl.drawLine()/input_scale),1)
            pixel_dist.insert(0, str(ratio))
            pixel_dist.configure(state='readonly')

            try:
                if auto_manual == 'auto':
                    
                    mdc.image_diam = [0,0]

                    if binState == 'NO':
                        adc.autoDetect(resized_img_cv2, int(param_dp.get()), int(param_minDist.get()), int(param_p1.get()), 
                            int(param_p2.get()), int(param_minDiam.get()), int(param_maxDiam.get()), ratio)

                    elif binState == 'YES':
                        adc.autoDetectBin(resized_img_cv2, int(binary_thresholdBar.get()),int(param_dp.get()), int(param_minDist.get()), int(param_p1.get()), 
                            int(param_p2.get()), int(param_minDiam.get()), int(param_maxDiam.get()), ratio)

                    output = adc.processCircles(True, resized_img_cv2, filename, ratio, mdc.image_diam)
                    
                    
                    if adc.detected_circles is None:
                        output_text.insert(tk.INSERT, '\n\nNo circles found!\n\n')  
                        return
                else:

                    manualDetect()
                    if reset == True or len(mdc.image_diam) == 1:
                        reset = False
                        return

                    mdc.image_diam.pop(0)

                    for items in range(len(mdc.image_diam)):
                        adc.rad_list.append(mdc.image_diam[items])

                    if "detected" in filename:
                        response = tk.messagebox.askyesno(title = 'Combine Manual Detection Data' , message = 'Do you wish to append the previous diameter values?')
                        if response == 1:
                            total_list = adc.rad_list
                            output = adc.processCircles(False, resized_img_cv2, filename, ratio, total_list)
                        else:
                            output = adc.processCircles(False, resized_img_cv2, filename, ratio, mdc.image_diam)
                    else:
                        output = adc.processCircles(False, resized_img_cv2, filename, ratio, mdc.image_diam)
                    
                output_text.insert(tk.INSERT, str(output) + '\n\n')
                output_text.yview_moveto(1)
                output_text.update()

                try:
                    maxRange.delete(0, 'end')
                    maxRange.insert(0, str(adc.max_range))
                    if int(maxRange.get()) < int(np.max(adc.rad_list)):
                        num = int(np.max(adc.rad_list)%int(interval_bins.get()))
                        addtoMaxRange = int(interval_bins.get()) - num
                        new_maxRange = int(np.max(adc.rad_list)) + addtoMaxRange
                    else:
                        new_maxRange = int(maxRange.get())
                except ValueError1:
                    output_text.insert(tk.INSERT, '\nERROR...Type: ValueError1!\n')
                    return


                maxRange.delete(0, 'end')
                maxRange.insert(0, str(new_maxRange))

                adc.histoPlot(filename, int(minRange.get()), new_maxRange, int(interval_bins.get()))
                
                histo_img = Image.open(filename[:-4] + '_histogram.png')
                width_histo, height_histo = histo_img.size
                
                factor_histo = width_histo/244
                histo_temp_img = histo_img.resize((int(width_histo/factor_histo), int(height_histo/factor_histo)))

                smaller_histo_img = ImageTk.PhotoImage(histo_temp_img)
                new_img_histo = tk.Label(frame_histo_show, image = smaller_histo_img).place(x=0,y=0)


                table_Data = adc.tableData()
                table = tkt.TableCanvas(frame_table, data = table_Data,
                        cellwidth=30, cellbackgr='white',
                        thefont=('Arial',10), width = 182, height = 384,
                        rowselectedcolor='#f8eba2')
                #If fresh install tkintertable, go to Tables.py and use only celltxt=str(celltxt), remove if statement
                table.show()

                mdc.image_diam = [0]
                mdc.image_prev = []

                if auto_manual == 'auto':
            
                    cv2.imshow("Detected Circles", adc.img)
                    cv2.waitKey(1)
                    if cv2.getWindowProperty('Detected Circles',1) == -1 :
                        cv2.destroyAllWindows()
                else: 
                    return
            #except NameError:
                #output_text.insert(tk.INSERT, '\nERROR...Type: NameError2!\n')
               # return
            except AttributeError:
                output_text.insert(tk.INSERT, '\nERROR...Type: AttributeError2!\n')
    output_text.yview_moveto(1)
    output_text.update()



def calibrateScaleBar():

    """
    Function to calibrate the scale bar in images
    """
    global filename, ratio, sb_location, resized_img_cv2, calibrated
    
    try:
        filename
    except NameError:
        output_text.insert(tk.INSERT, '\n\nERROR...Please upload an image first!\n\n')
        return

    if filename:

        mdl.load_img(resized_img_cv2, sb_location)

        while True:
            cv2.imshow("Cropped to measure scale-bar", mdl.cropped)
            
            key = cv2.waitKey(1) & 0xFF
                
            if key == ord("d"):
                mdl.b = mdl.b-1
                mdl.cropped = mdl.prev_cropped[mdl.b]
                mdl.cropped_prev.pop
                
            if cv2.getWindowProperty('Cropped to measure scale-bar',1) == -1 :
                cv2.destroyAllWindows()
                break

        pixel_dist.configure(state='normal')
        pixel_dist.delete(0, 'end')
        input_scale = float(str(scalebar.get()))

        ratio = np.round(abs(mdl.drawLine()/input_scale),1)

        pixel_dist.insert(0, str(ratio))
        pixel_dist.configure(state='readonly')

        if abs(mdl.drawLine()) > 1:
            calibrated = True


def manualDetect():

    """
    Function for manual detection mode
    """

    global filename, ratio, reset, resized_img_cv2
    
    try:
        filename
    except NameError:
        output_text.insert(tk.INSERT, '\nERROR...Type: NameError4!\n')
        filename = None

    if filename != None:

        if filename:
            try:
                mdc.load_img(resized_img_cv2, ratio)
            except NameError:
                output_text.insert(tk.INSERT, '\nERROR...Type: NameError5!\n')
                reset = True
                return

            last_value = 1
            mdc.initialize()

            while True:
                cv2.imshow("Manual Draw Mode", mdc.image)

                if len(mdc.diamCircles(True)) != last_value :

                    if len(mdc.image_diam)>1:

                        currVal = mdc.image_diam[len(mdc.image_diam)-1]
     
                        output_text.yview_moveto(1)
                        output_text.insert(tk.INSERT, '\n'+str(currVal))
                        output_text.update()

                        last_value = len(mdc.diamCircles(True))

                key = cv2.waitKey(1) & 0xFF
                    
                if key == ord("d") or key == ord("D"):
                    try:
                        output_text.yview_moveto(1)
                        output_text.delete('end -1 lines', 'end')
                        output_text.update()
                        last_value = len(mdc.diamCircles(False))
                        mdc.image = mdc.prev_img[mdc.b]

                    except IndexError:
                        output_text.insert(tk.INSERT, '\nERROR...Type: IndexError1!\n')
                        cv2.destroyAllWindows()
                        break

                elif cv2.getWindowProperty('Manual Draw Mode',1) == -1 :
                    break

        new_name = filename[:-4] + '_detected' + filename[-4:]
        cv2.imwrite(new_name,mdc.image)
        cv2.destroyAllWindows()
           

def rd_button_clicked(value):

    """
    Function to activate auto/manual detection mode
    """

    global auto_manual
    if value == 'auto':
        auto_manual = value
    else:
        auto_manual = value         

def turn_binary(state):

    """
    Function to convert image to binary image (black and white only)
    """

    global open_img, window_img, adj_height, binImg, binary_state, binState
    try:
        open_img
    except NameError:
        open_img = None
    if open_img != None:

        window_img = ImageTk.PhotoImage(open_img)
        show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
        binState = yesNoState.get()
        state = binState
        thresholdBar = int(binary_thresholdBar.get())
 
        if state == 'YES':
            img = np.asarray(open_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thres,binImg = cv2.threshold(img, thresholdBar, 255, cv2.THRESH_BINARY)
            new_img = Image.fromarray(binImg)
            window_img = ImageTk.PhotoImage(new_img)
            show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
            return 'YES'

        elif state == 'NO':
            return 'NO'


#Binary image threshold bar on GUI
binary_thresholdBar = tk.Scale(frame_binary, from_ = 1, to = 254, orient = 'horizontal', length = 120,  command = turn_binary)
binary_thresholdBar.grid(row=0, column=4, columnspan = 3, padx=1, pady=1, sticky = 'w')
binary_thresholdBar.set(127)

binary_state = tk.Checkbutton(frame_binary, text='TURN ON', variable = yesNoState, onvalue='YES', offvalue='NO', state = 'disabled', command=lambda: turn_binary(yesNoState))
binary_state.grid(row=1, column=4, columnspan = 3, padx=1, pady=1)

detect_method = tk.StringVar()
auto_manual = 'auto'
detect_method.set('auto detect')

#Auto/Manual detect GUI button
tk.Radiobutton(frame_rdbutton, text="MANUAL DETECT - Manually draw circles to get diameter values",
               variable=detect_method, value='manual detect', command=lambda: rd_button_clicked('manual')).pack(anchor='w')
tk.Radiobutton(frame_rdbutton, text="AUTO DETECT - Uses 'Circle Hough Transform' to detect circles",
               variable=detect_method, value='auto detect', command=lambda: rd_button_clicked('auto')).pack(anchor='w')
 
calibrate_button = tk.Button(frame_scalebar, text='Calibrate', relief='raised', borderwidth = 2, command=calibrateScaleBar)
calibrate_button.config(height=1, width=9, font=('Helvetica', '8'))
calibrate_button.grid(row = 3, column = 2, columnspan = 4, padx=1, pady=2, sticky ='e')
 
img_button = tk.Button(frame_upload, text='CLICK\nto upload an image', relief='raised', command=open_file)
img_button.config(height=2, width=15, font=('Helvetica', '10'))
img_button.pack(fill='both')
 
start_button = tk.Button(frame_start, text='START\nAuto/Manual Mode', relief='raised', command=start_state)
start_button.config(height=2, width=15, font=('Helvetica', '10'))
start_button.pack(fill='both')
 
credit = tk.Label(root, text='R.Lu (v1.3.2), 2020', font='consolas 8 bold')
credit.grid(row=69, column=11, padx = 5,sticky = 'ne')


#Pop up window when GUI X-button is pressed
def closing():
    if tk.messagebox.askokcancel("Exit Program", "Do you wish to quit the program?"):
        cv2.destroyAllWindows()
        root.quit()

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()


