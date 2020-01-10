import tkinter as tk
from PIL import ImageTk, Image
import tkinter.scrolledtext as tkst
from tkinter import filedialog
import AutoDetectCircle_OutWindow as adc
import cv2
import matplotlib.pyplot as plt
import tkintertable as tkt
 
root = tk.Tk()
root.title("Spherical Detection Program")
# oot.iconbitmap()
root.geometry('1100x900')
# root.resizable(0, 0)
# root.pack_propagate(0)
 
global temp_img, auto_manual, start_circle, img_conver, output, new_img_histo, frame_histo_show, sw_img, cv2_img, filename
 
output = 'Output results will display below...\n----------------------------------------\n'
start_state = False
 
frame_logo = tk.LabelFrame(root, width=70)
frame_logo.grid(row=0, column=0, rowspan=1, columnspan=10, padx=5, pady=5)
 
logo_img = ImageTk.PhotoImage(Image.open('circled1.png'))
logo_show = tk.Label(frame_logo, image=logo_img).pack()
 
frame_intro = tk.LabelFrame(root, width=80)
frame_intro.grid(row=2, column=0, rowspan=2, columnspan=8, padx=5, pady=5)
 
intro_text = tkst.ScrolledText(frame_intro, wrap=tk.WORD, width=70, height=14, undo=False)
intro_text['font'] = ('consolas', '10')
intro_text.insert(tk.INSERT,
                  "Welcome to the Spherical Detection program!\n\nThis software program uses the 'Circle Hough Transform' (CHT) feature extraction technique to detect circles in images. "
                  "Circle candidates are produced by 'voting' in the Hough parameter space and selecting the local maxima in the accumulator matrix. "
                  "Hence, not all circles may be detected and the parameters have to be optimized to prevent over-detection/under-detection of circles."
                  "\n-----------------------------------------------"
                  "\nManual circle detection is also an option. Simply 'click and drag' from one side of a circle to the other side in the pop-up image window."
                  "\n\nReadings:\nhttps://en.wikipedia.org/wiki/Circle_Hough_Transform\n\nDescription of Hough Circle parameters:\nhttps://docs.opencv.org/3.4/d3/de5/tutorial_js_houghcircles.html")
 
intro_text.pack(expand=True, fill='both')
 
frame_output = tk.LabelFrame(root, bg='BLACK', width=85)
frame_output.grid(row=0, column=8, rowspan=8, columnspan=4, padx=10, pady=10, sticky='n')
 
output_text = tkst.ScrolledText(frame_output, wrap=tk.WORD, width=55, height=33, undo=False)
output_text['font'] = ('consolas', '10')
output_text.insert(tk.INSERT, str(output))
output_text.pack(expand=True, anchor='n')
 
frame_rdbutton = tk.LabelFrame(root, width=70, padx=5, pady=5)
frame_rdbutton.grid(row=4, column=0, rowspan=2, columnspan=6, padx=10, pady=10, sticky='w')
frame_start = tk.LabelFrame(root, width=70, padx=5, pady=5)
frame_start.grid(row=4, column=6, rowspan=2, columnspan=1, padx=5, pady=5, sticky='w')
frame_upload = tk.LabelFrame(root, width=70, padx=5, pady=5)
frame_upload.grid(row=6, rowspan=2, column=6, columnspan=1, sticky='w')
 
frame_preview = tk.LabelFrame(root)
frame_preview.grid(row=9, column=4, rowspan=4, columnspan=5, padx=5, pady=5)

frame_histo_show = tk.LabelFrame(root, width = 70)
frame_histo_show.grid(row=9, column = 0, rowspan = 2, columnspan = 4, padx = 5, pady = 5)

frame_table = tk.LabelFrame(root)
frame_table.grid(row = 9, column = 10, rowspan = 2, columnspan = 3, padx= 5, pady=5)

table_data = {'rec1': {'col1': 99.88, 'col2': 108.79},
'rec2': {'col1': 99.88, 'col2': 108.79}}

table = tkt.TableCanvas(frame_table, data = table_data,
            cellwidth=30, cellbackgr='white',
            thefont=('Arial',11), rows=15, cols=3, width = 200,
            rowselectedcolor='#f8eba2')
table.show()


smaller_histo_img = ImageTk.PhotoImage(Image.open('black320x240.png'))
new_img_histo = tk.Label(frame_histo_show,image = smaller_histo_img)
new_img_histo.pack()


detect_method = tk.StringVar()
auto_manual = 'auto'
detect_method.set('auto detect')
 
tk.Radiobutton(frame_rdbutton, text="MANUAL DETECT - Manually draw circles to get diameter values",
               variable=detect_method, value='manual detect', command=lambda: rd_button_clicked('manual')).pack(
    anchor='w')
tk.Radiobutton(frame_rdbutton, text="AUTO DETECT - Uses 'Circle Hough Transform' to detect circles",
               variable=detect_method, value='auto detect', command=lambda: rd_button_clicked('auto')).pack(anchor='w')
 
 
def rd_button_clicked(value):
    global auto_manual
    if value == 'auto':
        auto_manual = value
        print(auto_manual + ", inside rd_button funct1")
    else:
        auto_manual = value
        print(auto_manual + ", inside rd_button funct2")
 
 
frame_HoughCircle = tk.LabelFrame(root, text='Hough Circle Parameters', width=70, padx=5, pady=5)
frame_HoughCircle.grid(row=6, column=0, rowspan=2, columnspan=6, padx=5, pady=5, sticky='w')
 
param_minDist = tk.Entry(frame_HoughCircle, width=5)
param_minDist.grid(row=0, column=1, padx=1, pady=1)
label_minDist = tk.Label(frame_HoughCircle, text='Min Distance:')
label_minDist.grid(row=0, column=0, padx=1, pady=1)
 
param_dp = tk.Entry(frame_HoughCircle, width=5)
param_dp.grid(row=1, column=1, padx=1, pady=1)
label_dp = tk.Label(frame_HoughCircle, text='Accum/Res Ratio (dp):')
label_dp.grid(row=1, column=0, padx=1, pady=1)
 
param_minR = tk.Entry(frame_HoughCircle, width=5)
param_minR.grid(row=0, column=3, padx=1, pady=1)
label_minR = tk.Label(frame_HoughCircle, text=' Min Radius:')
label_minR.grid(row=0, column=2, padx=1, pady=1)
 
param_maxR = tk.Entry(frame_HoughCircle, width=5)
param_maxR.grid(row=1, column=3, padx=1, pady=1)
label_maxR = tk.Label(frame_HoughCircle, text=' Max Radius:')
label_maxR.grid(row=1, column=2, padx=1, pady=1)
 
param_p1 = tk.Entry(frame_HoughCircle, width=5)
param_p1.grid(row=0, column=5, padx=1, pady=1)
label_p1 = tk.Label(frame_HoughCircle, text=' Param1:')
label_p1.grid(row=0, column=4, padx=1, pady=1)
 
param_p2 = tk.Entry(frame_HoughCircle, width=5)
param_p2.grid(row=1, column=5, padx=1, pady=1)
label_p2 = tk.Label(frame_HoughCircle, text=' Param2:')
label_p2.grid(row=1, column=4, padx=1, pady=1)
 
frame_histo_param = tk.LabelFrame(root, text='Histogram Parameters', width=70, padx=5, pady=5)
frame_histo_param.grid(row=11, column=0, rowspan=1, columnspan=4, padx=5, pady=5, sticky = 's')
 
param_bins = tk.Entry(frame_histo_param, width=7)
param_bins.grid(row=0, column=1, padx=1, pady=1)
label_bins = tk.Label(frame_histo_param, text='# of Bins:')
label_bins.grid(row=0, column=0, padx=1, pady=1)
label_bins_eg = tk.Label(frame_histo_param, text='e.g. 20 or [5,10,15,20...50]')
label_bins_eg.grid(row=0, column=2, padx=1, pady=1, stick='w')
 
param_rwidth = tk.Entry(frame_histo_param, width=7)
param_rwidth.grid(row=1, column=1, padx=1, pady=1)
label_rwidth = tk.Label(frame_histo_param, text='Bar Width:')
label_rwidth.grid(row=1, column=0, padx=1, pady=1)
label_rwidth_eg = tk.Label(frame_histo_param, text='e.g. # between 0 - 1.0')
label_rwidth_eg.grid(row=1, column=2, padx=1, pady=1, stick='w')
 
black_img = Image.open('black300.png')
temp_img = ImageTk.PhotoImage(black_img)
placeholder_img = tk.Label(frame_preview, image=temp_img).pack()
 
 
def open_file():
    global temp_jpg, window_img, placeholder_img, img_conver, show_img, img_width, img_height, filename

    black_img = Image.open('black300.png')
    temp_img = ImageTk.PhotoImage(black_img)
    placeholder_img = tk.Label(frame_preview, image=temp_img, bg ='black').place(x=0, y=0)
 
    filename = filedialog.askopenfilename(initialdir='C:\\', title="Select a file",
                                          filetypes=(
                                          ("jpg Files", "*jpg"), ("png Files", "*png"), ("tif Files", "*tif")))
    if filename:
        img_conver = filename[:-3] + 'jpg'
        try:  
            temp_jpg = Image.open(filename).convert("RGB")
        except IOError: 
            pass
     
        img_width, img_height = temp_jpg.size
        print(img_width, img_height)
     
        max_wh = max(img_width, img_height)
        factor = max_wh / 300
        print(factor)
        temp_jpg = temp_jpg.resize((int(img_width / factor), int(img_height / factor)))
        adj_height = (300 - (img_height / factor)) / 2
        print(adj_height)
        window_img = ImageTk.PhotoImage(temp_jpg)
        show_img = tk.Label(frame_preview, bg ="black", image=window_img).place(x=0, y=adj_height)
        print(auto_manual + ", inside open_file funct1")

 
def start_state():
    global img_conver, filename, temp_img, detected_img, output, smaller_histo_img, new_img_histo, cv2_img, img_width, img_height
    start_circle = True
    output = adc.autoDetect(filename)

    if auto_manual == 'auto' and start_circle == True:
        print(auto_manual + ", inside open_file funct2")
    output_text.insert(tk.INSERT, str(output) + '\n\n')
 
    histo_img = Image.open(filename[:-4] + '_histogram.png')
    width_histo, height_histo = histo_img.size
    
    factor_histo = width_histo/320
    histo_temp_img = histo_img.resize((int(width_histo/factor_histo), int(height_histo/factor_histo)))

    smaller_histo_img = ImageTk.PhotoImage(histo_temp_img)
    new_img_histo = tk.Label(frame_histo_show, image = smaller_histo_img).place(x=0,y=0)

    max_wh = max(img_width, img_height)
    if max_wh > 1100:
        factor = max_wh / 1000
    elif max_wh > 500 and max_wh < 1000:
        factor = max_wh
    else:
        factor = max_wh / 700
    
    cv2_img = adc.img
    cv2.namedWindow("Detected Circles", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detected Circles', int(img_width / factor), int(img_height / factor))
    cv2.imshow("Detected Circles", cv2_img)
    cv2.waitKey(1)
    if cv2.getWindowProperty('Detected Circles',1) == -1 :
        cv2.destroyAllWindows()
    print('break, destroyed all windows\n')
    
 
img_button = tk.Button(frame_upload, text='CLICK\nto upload an image', relief='raised', command=open_file)
img_button.config(height=2, width=15, font=('Helvetica', '10'))
img_button.pack(fill='both')
 
start_button = tk.Button(frame_start, text='START\nAuto/Manual Mode', relief='raised', command=start_state)
start_button.config(height=2, width=15, font=('Helvetica', '10'))
start_button.pack(fill='both')
 
credit = tk.Label(root, text='R.Lu (v1.0.0), 2020', font='consolas 10 bold')
credit.grid(row=12, column=11, sticky='se')

table_label = tk.Label(root, text ='To export table: Right-click --> File --> Export CSV')
table_label.grid(row = 11, column = 9, columnspan = 2)

def closing():
    if tk.messagebox.askokcancel("Exit Program", "Do you wish to quit the program?"):
        root.quit()

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()

