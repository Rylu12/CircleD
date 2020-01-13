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

 
root = tk.Tk()
root.title("Spherical Detection Program")
# oot.iconbitmap()
root.geometry('1180x780')
# root.resizable(0, 0)
# root.pack_propagate(0)
 
global temp_img, auto_manual, start_circle, img_conver, output, new_img_histo, frame_histo_show, sw_img, cv2_img, filename
global accum_ratio, min_dist, p1, p2, minDiam, maxDiam, binImg, table_Data, table

reset = False

table_Data = {'rec1': {'Col1': 'Diam.', 'Col2': 'values', 'Col3': 'will'}, 'rec2':{'Col1': 'go', 'Col2': 'here', 'Col3': ' '}, 
                'rec3': {'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 'rec4':{'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 
                'rec5':{'Col1': ' ', 'Col2': ' ', 'Col3': ' '}, 'rec6': {'Col1': ' ', 'Col2': ' ', 'Col3': ' '}}

output = 'Output results will display below...\n----------------------\n'
start_state = False

frame_logo = tk.LabelFrame(root, width=80)
frame_logo.grid(row=0, column=0, rowspan = 10, columnspan=7, padx=10, pady=5)
 
logo_img = ImageTk.PhotoImage(Image.open('circled1.png'))
logo_show = tk.Label(frame_logo, image=logo_img).pack()
 
frame_intro = tk.LabelFrame(root, width=80)
frame_intro.grid(row=10, column=0, rowspan=20, columnspan=7, padx=10, pady=5)
 
intro_text = tkst.ScrolledText(frame_intro, wrap=tk.WORD, width=70, height=11, undo=False)
intro_text['font'] = ('consolas', '10')
intro_text.insert(tk.INSERT,
                  "Welcome to the Spherical Detection program!\n\nThis software program uses the 'Circle Hough Transform' (CHT) feature extraction technique to detect circles in images. "
                  "Circle candidates are produced by 'voting' in the Hough parameter space and selecting the local maxima in the accumulator matrix. "
                  "Hence, not all circles may be detected and the parameters have to be optimized to prevent over-detection/under-detection of circles."
                  "\n-----------------------------------------------"
                  "\nManual circle detection is also an option. Simply 'click and drag' from one side of a circle to the other side in the pop-up image window."
                  "\n\nReadings:\nhttps://en.wikipedia.org/wiki/Circle_Hough_Transform\n\nDescription of Hough Circle parameters:\nhttps://docs.opencv.org/3.4/d3/de5/tutorial_js_houghcircles.html")
 
intro_text.pack(expand=True, fill='both')
 
frame_output = tk.LabelFrame(root, bg='BLACK', width=30)
frame_output.grid(row=0, column=8, rowspan=65, columnspan=2, padx=10, pady=5, sticky='n')
 
output_text = tkst.ScrolledText(frame_output, wrap=tk.WORD, width=25, height=30, undo=False)
output_text['font'] = ('consolas', '11')
output_text.insert(tk.INSERT, str(output))
output_text.pack(expand=True, anchor='n')
 
frame_rdbutton = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_rdbutton.grid(row=30, column=0, rowspan=10, columnspan=5, padx=10, pady=5, sticky='w')
frame_start = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_start.grid(row=30, column=5, rowspan=10, columnspan=1, padx=0, pady=5)
frame_upload = tk.LabelFrame(root, width=70, padx=10, pady=5)
frame_upload.grid(row=40, rowspan=10, column=5, columnspan=1, padx=0, pady=5)
 
frame_preview = tk.LabelFrame(root)
frame_preview.grid(row=50, column=4, rowspan=40, columnspan=3, padx=10, pady=5, sticky = 'nw')

frame_binary = tk.LabelFrame(root, text = "Binary Filter Mode")
frame_binary.grid(row=75, column=8, rowspan = 15, columnspan=3, padx=10, pady=5, sticky = 'nw')

frame_histo_show = tk.LabelFrame(root)
frame_histo_show.grid(row=60, column = 0, rowspan = 30, columnspan = 4, padx=10, pady=5, sticky = 'nw')

frame_table = tk.LabelFrame(root)
frame_table.grid(row = 0, column = 10,  rowspan = 65, columnspan = 2, padx=10, pady=5, sticky = 'n')

table_label = tk.Label(root, text ='To Export Table:\n------\nRight-Click\n|\nV\nFile\n|\nV\nExport CSV')
table_label.grid(row = 65, rowspan = 15, column = 11, sticky = 'n')

smaller_histo_img = ImageTk.PhotoImage(Image.open('black320x240.png'))
new_img_histo = tk.Label(frame_histo_show,image = smaller_histo_img)
new_img_histo.pack()

 
frame_HoughCircle = tk.LabelFrame(root, text='Hough Circle Parameters', width=70, padx=10, pady=5)
frame_HoughCircle.grid(row=40, column=0, rowspan = 10, columnspan=5, padx=10, pady=5, sticky='w')
 
param_minDist = tk.Entry(frame_HoughCircle, width=5)
param_minDist.insert(0, str(adc.min_dist))
param_minDist.grid(row=0, column=1, padx=1, pady=1)
label_minDist = tk.Label(frame_HoughCircle, text='Min Distance (um):')
label_minDist.grid(row=0, column=0, padx=1, pady=1)
 
param_dp = tk.Entry(frame_HoughCircle, width=5)
param_dp.insert(0, str(adc.accum_ratio))
param_dp.grid(row=1, column=1, padx=1, pady=1)
label_dp = tk.Label(frame_HoughCircle, text='Accum/Res Ratio (dp):')
label_dp.grid(row=1, column=0, padx=1, pady=1)
 
param_minDiam = tk.Entry(frame_HoughCircle, width=5)
param_minDiam.insert(0, str(adc.minDiam))
param_minDiam.grid(row=0, column=3, padx=1, pady=1)
label_minDiam = tk.Label(frame_HoughCircle, text=' Min Diam (um):')
label_minDiam.grid(row=0, column=2, padx=1, pady=1)
 
param_maxDiam = tk.Entry(frame_HoughCircle, width=5)
param_maxDiam.insert(0, str(adc.maxDiam))
param_maxDiam.grid(row=1, column=3, padx=1, pady=1)
label_maxDiam = tk.Label(frame_HoughCircle, text=' Max Diam (um):')
label_maxDiam.grid(row=1, column=2, padx=1, pady=1)
 
param_p1 = tk.Entry(frame_HoughCircle, width=5)
param_p1.insert(0, str(adc.p1))
param_p1.grid(row=0, column=5, padx=1, pady=1)
label_p1 = tk.Label(frame_HoughCircle, text=' Param1:')
label_p1.grid(row=0, column=4, padx=1, pady=1)
 
param_p2 = tk.Entry(frame_HoughCircle, width=5)
param_p2.insert(0, str(adc.p2))
param_p2.grid(row=1, column=5, padx=1, pady=1)
label_p2 = tk.Label(frame_HoughCircle, text=' Param2:')
label_p2.grid(row=1, column=4, padx=1, pady=1)


frame_scalebar = tk.LabelFrame(root, text = "Calibrates Pixel/Distance Ratio",width=70, padx=10, pady=5)
frame_scalebar.grid(row=64, column=8,  rowspan = 11, columnspan=3, padx=10, pady=5, sticky='w')

scalebar = tk.Entry(frame_scalebar, width=10)
scalebar.insert(0, str(adc.scalebar))
scalebar.grid(row=2, column=4, columnspan = 2, padx=1, pady=1, sticky = 'w')
label_scalebar = tk.Label(frame_scalebar, text='Known distance of scale-bar (um):')
label_scalebar.grid(row=2, column=0, columnspan = 4, padx=1, pady=1)

pixel_dist = tk.Entry(frame_scalebar, width=10, state = 'readonly')
pixel_dist.grid(row=3, column=1, padx=1, pady=1, sticky = 'w')
label_pixel_dist = tk.Label(frame_scalebar, text='Pixel/Distance Ratio:')
label_pixel_dist.grid(row=3, column=0, padx=1, pady=1, sticky = 'w')



frame_histo_param = tk.LabelFrame(root, text='Histogram Parameters', width=70, padx=10, pady=5)
frame_histo_param.grid(row=50, column=0, rowspan = 5, columnspan=4, padx=10, pady=5, sticky = 'w')
 
interval_bins = tk.Entry(frame_histo_param, width=5)
interval_bins.insert(0, str(adc.intervals))
interval_bins.grid(row=0, column=1, padx=1, pady=1)
label_bins = tk.Label(frame_histo_param, text='Intervals:')
label_bins.grid(row=0, column=0, padx=1, pady=1)
 
minRange = tk.Entry(frame_histo_param, width=5)
minRange.insert(0, str(adc.min_range))
minRange.grid(row=0, column=3, padx=1, pady=1)
label_minRange = tk.Label(frame_histo_param, text='Min Range:')
label_minRange.grid(row=0, column=2, padx=1, pady=1)

maxRange = tk.Entry(frame_histo_param, width=5)
maxRange.insert(0, str(adc.max_range))
maxRange.grid(row=0, column=5, padx=1, pady=1)
label_maxRange = tk.Label(frame_histo_param, text='Max Range:')
label_maxRange.grid(row=0, column=4, padx=1, pady=1)


 
black_img = Image.open('black300.png')
temp_img = ImageTk.PhotoImage(black_img)
placeholder_img = tk.Label(frame_preview, image=temp_img).pack()
 


table = tkt.TableCanvas(frame_table, data = table_Data,
            cellwidth=30, cellbackgr='white',
            thefont=('Arial',10), width = 180, height = 520,
            rowselectedcolor='#f8eba2')
table.show()
 


def open_file():
    global open_img, window_img, placeholder_img, show_img, img_width, img_height, filename, adj_height

    highLowOff.set('OFF')
    black_img = Image.open('black300.png')
    temp_img = ImageTk.PhotoImage(black_img)
    placeholder_img = tk.Label(frame_preview, image=temp_img, bg ='black').place(x=0, y=0)
 
    filename = filedialog.askopenfilename(initialdir='C:\\', title="Select a file",
                                          filetypes=(
                                          ("jpg Files", "*jpg"), ("png Files", "*png"), ("tif Files", "*tif")))
    resize = False
    if filename:
        try:  
            open_img = Image.open(filename).convert("RGB")
        except IOError: 
            pass
     
        img_width, img_height = open_img.size
        
        max_wh = max(img_width, img_height)

        if max_wh > 1100:
            output_text.insert(tk.INSERT, '\nYour image is too big (>1100 pixels)! A scaled-down copy is made and will be used instead.\n\n')
            resize_copy = max_wh/1100
            resize_img = open_img.resize((int(img_width/resize_copy), int(img_height/resize_copy)))
            filename = (filename[:-4] + '_smaller' + filename[-4:])
            resize_img.save(filename) 

        elif max_wh <500:
            output_text.insert(tk.INSERT, '\nYour image is too small (<500 pixels)! A scaled-up copy is made and will be used instead.\n\n')
            resize_copy = max_wh/1000
            resize_img = open_img.resize((int(img_width/resize_copy), int(img_height/resize_copy)))
            filename = (filename[:-4] + '_bigger' + filename[-4:])
            resize_img.save(filename)    

        factor = max_wh/300
        

        open_img = open_img.resize((int(img_width / factor), int(img_height / factor)))

        adj_height = (300 - (img_height / factor)) / 2

        window_img = ImageTk.PhotoImage(open_img)
        show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)


def turn_binary():
    global filename, open_img, window_img, adj_height, binImg
    try:
        open_img
    except NameError:
        open_img = None
    if open_img != None:

        window_img = ImageTk.PhotoImage(open_img)
        show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
        state = highLowOff.get()

        if state == 'HIGH':
            img = np.asarray(open_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thres,binImg = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
            new_img = Image.fromarray(binImg)
            window_img = ImageTk.PhotoImage(new_img)
            show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
            return 'HIGH'

        elif state == 'LOW':
            img = np.asarray(open_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thres,binImg = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            new_img = Image.fromarray(binImg)
            window_img = ImageTk.PhotoImage(new_img)
            show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
            return 'LOW'

        elif state == 'OFF':
            return 'OFF'

def start_state():
    global filename, temp_img, detected_img, output, smaller_histo_img, ratio, reset
    global new_img_histo, cv2_img, img_width, img_height, bin_img, table_Data, table


    try:
        filename
    except NameError:
        filename = None
    if filename != None:
        if filename:
    
            if auto_manual == 'auto':
                if turn_binary() == 'OFF':
                    adc.autoDetect(filename, int(param_dp.get()), int(param_minDist.get()), int(param_p1.get()), 
                        int(param_p2.get()), int(param_minDiam.get()), int(param_maxDiam.get()), ratio)
                elif turn_binary() == 'HIGH':
                    adc.autoDetectBin(filename, 150,int(param_dp.get()), int(param_minDist.get()), int(param_p1.get()), 
                        int(param_p2.get()), int(param_minDiam.get()), int(param_maxDiam.get()), ratio)
                elif turn_binary() == 'LOW':
                    adc.autoDetectBin(filename, 100,int(param_dp.get()), int(param_minDist.get()), int(param_p1.get()), 
                        int(param_p2.get()), int(param_minDiam.get()), int(param_maxDiam.get()), ratio)

                output = adc.processCircles(filename, ratio, mdc.image_diam)
            
                if adc.detected_circles is None:
                    output_text.insert(tk.INSERT, '\nNo Circles Found!\n')  
                    return
            else:
                
                manualDetect()
                if reset == True:
                    reset = False
                    return

                mdc.image_diam.pop(0)

                for items in range(len(mdc.image_diam)):
                    adc.rad_list.append(mdc.image_diam[items])
                
                output = adc.processCircles(filename, ratio, mdc.image_diam)
                
            output_text.insert(tk.INSERT, str(output) + '\n\n')
            try:
                if int(maxRange.get()) < int(np.max(mdc.image_diam)):
                    num = int(np.max(mdc.image_diam)%int(interval_bins.get()))
                    addtoMaxRange = int(interval_bins.get()) - num
                    new_maxRange = int(np.max(mdc.image_diam)) + addtoMaxRange
                else:
                    new_maxRange = int(maxRange.get())
            except ValueError:
                return

            adc.histoPlot(filename, int(minRange.get()), new_maxRange, int(interval_bins.get()))
            maxRange.delete(0, 'end')
            maxRange.insert(0, str(new_maxRange))
            histo_img = Image.open(filename[:-4] + '_histogram.png')
            width_histo, height_histo = histo_img.size
            
            factor_histo = width_histo/320
            histo_temp_img = histo_img.resize((int(width_histo/factor_histo), int(height_histo/factor_histo)))

            smaller_histo_img = ImageTk.PhotoImage(histo_temp_img)
            new_img_histo = tk.Label(frame_histo_show, image = smaller_histo_img).place(x=0,y=0)


            table_Data = adc.tableData()
            table = tkt.TableCanvas(frame_table, data = table_Data,
                    cellwidth=30, cellbackgr='white',
                    thefont=('Arial',10), width = 180, height = 520,
                    rowselectedcolor='#f8eba2')

            table.show()

            mdc.image_diam = [0]
            mdc.image_prev = []

            if auto_manual == 'auto':
                max_wh = max(img_width, img_height)
                if max_wh > 800:
                    factor = max_wh / 800
                elif max_wh > 600 and max_wh < 800:
                    factor = max_wh
                else:
                    factor = max_wh/800
                
                cv2_img = adc.img
                cv2.namedWindow("Detected Circles", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Detected Circles', int(img_width / factor), int(img_height / factor))
                cv2.imshow("Detected Circles", cv2_img)
                cv2.waitKey(1)
                if cv2.getWindowProperty('Detected Circles',1) == -1 :
                    cv2.destroyAllWindows()
            else: 
                return


def calibrateScaleBar():
    global filename, ratio
    
    try:
        filename
    except NameError:
        filename = None

    if filename != None:

        if filename:

            mdl.load_img(filename)

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


def manualDetect():
    global filename, ratio, reset
    
    try:
        filename
    except NameError:
        filename = None

    if filename != None:

        if filename:
            try:
                mdc.load_img(filename, ratio)
            except NameError:
                output_text.insert(tk.INSERT, '\nERROR...PLEASE CALIBRATE PIXEL/DISTANCE VALUE FIRST!\n')
                reset = True
                return

            last_value = 0

            while True:
                cv2.imshow("Manual Draw Mode", mdc.image)
                
                if mdc.diamCircles(True) != last_value:

                    last_value = mdc.diamCircles(True)

                key = cv2.waitKey(1) & 0xFF
                    
                if key == ord("d") or key == ord("D"):
                    try:

                        mdc.diamCircles(False)
                        mdc.image = mdc.prev_img[mdc.b]

                    except IndexError:
                        output_text.insert(tk.INSERT, '\nINDEX ERROR... PLEASE RESTART PROGRAM!\n')  
                        cv2.destroyAllWindows()
                        break

                elif cv2.getWindowProperty('Manual Draw Mode',1) == -1 :
                    break    
        new_name = filename[:-4] + '_detected' + filename[-4:]
        cv2.imwrite(new_name,mdc.image)
        cv2.destroyAllWindows()
                    


detect_method = tk.StringVar()
auto_manual = 'auto'
detect_method.set('auto detect')
 
tk.Radiobutton(frame_rdbutton, text="MANUAL DETECT - Manually draw circles to get diameter values",
               variable=detect_method, value='manual detect', command=lambda: rd_button_clicked('manual')).pack(anchor='w')
tk.Radiobutton(frame_rdbutton, text="AUTO DETECT - Uses 'Circle Hough Transform' to detect circles",
               variable=detect_method, value='auto detect', command=lambda: rd_button_clicked('auto')).pack(anchor='w')
 
 
def rd_button_clicked(value):
    global auto_manual
    if value == 'auto':
        auto_manual = value
    else:
        auto_manual = value

highLowOff = tk.StringVar()
highLowOff.set('OFF')
binary = tk.Radiobutton(frame_binary, text='Activate Low-Binary Filter', variable = highLowOff, value='LOW', command= turn_binary)
binary.grid(row=0, column=4, columnspan = 3, padx=1, pady=1, sticky = 'w')
binary = tk.Radiobutton(frame_binary, text='Activate High-Binary Filter', variable = highLowOff, value='HIGH', command=turn_binary)
binary.grid(row=1, column=4, columnspan = 3, padx=1, pady=1, sticky = 'w')
binary = tk.Radiobutton(frame_binary, text='Binary Filter is OFF', variable = highLowOff, value='OFF', command=turn_binary)
binary.grid(row=2, column=4, columnspan = 3, padx=1, pady=1, sticky = 'w')


calibrate_button = tk.Button(frame_scalebar, text='Calibrate', relief='raised', borderwidth = 2, command=calibrateScaleBar)
calibrate_button.config(height=1, width=9, font=('Helvetica', '8'))
calibrate_button.grid(row = 3, column = 2, columnspan = 4, padx=1, pady =2, sticky ='e')
 

img_button = tk.Button(frame_upload, text='CLICK\nto upload an image', relief='raised', command=open_file)
img_button.config(height=2, width=15, font=('Helvetica', '10'))
img_button.pack(fill='both')
 
start_button = tk.Button(frame_start, text='START\nAuto/Manual Mode', relief='raised', command=start_state)
start_button.config(height=2, width=15, font=('Helvetica', '10'))
start_button.pack(fill='both')
 
credit = tk.Label(root, text='R.Lu (v1.0.0), 2020', font='consolas 10 bold')
credit.grid(row=89, column=11, sticky='se')

def closing():
    if tk.messagebox.askokcancel("Exit Program", "Do you wish to quit the program?"):
        cv2.destroyAllWindows()
        root.quit()

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()

