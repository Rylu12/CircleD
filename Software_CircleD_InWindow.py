import tkinter as tk
from PIL import ImageTk, Image
import tkinter.scrolledtext as tkst
from tkinter import filedialog
import AutoDetectCircle as adc

root = tk.Tk()
root.title("Spherical Detection Program")
root.iconbitmap(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\Udemy_Courses\Python_Computer_Vision\DATA\reeses_puffs.ico')
root.geometry('1180x800')
#root.resizable(0, 0)
#root.pack_propagate(0)

global temp_img, auto_manual, start_circle, filename, output, new_img_histo, frame_SW, sw_img

output = 'Output results will display below...\n----------------------------------------\n'
start_state = False

frame_logo = tk.LabelFrame(root, width =70)
frame_logo.grid(row=1, column = 0, columnspan = 3, padx = 5, pady=5)

logo_img = ImageTk.PhotoImage(Image.open(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\circled1.png'))
logo_show = tk.Label(frame_logo, image = logo_img).pack()

frame_NW = tk.LabelFrame(root, width = 80)
frame_NW.grid(row = 2, column = 0, rowspan = 2, columnspan= 3, padx = 5, pady = 5)

intro_text = tkst.ScrolledText(frame_NW, wrap = tk.WORD, width = 70, height = 13, undo = False)
intro_text['font'] = ('consolas', '10')
intro_text.insert(tk.INSERT, "Welcome to the Spherical Detection program!\n\nThis software program uses the 'Circle Hough Transform' (CHT) feature extraction technique to detect circles in images. "
	"Circle candidates are produced by 'voting' in the Hough parameter space and selecting the local maxima in the accumulator matrix. " 
	"Hence, not all circles may be detected and the parameters have to be optimized to prevent over-detection/under-detection of circles."
	"\n-----------------------------------------------"
	"\nManual circle detection is also an option. Simply 'click and drag' from one side of a circle to the other side."
	"\n\nResources:\nhttps://en.wikipedia.org/wiki/Circle_Hough_Transform\nhttps://docs.opencv.org/3.4/d3/de5/tutorial_js_houghcircles.html")

intro_text.pack(expand=True, fill= 'both')


frame_SE = tk.LabelFrame(root, bg = 'BLACK', width = 85)
frame_SE.grid(row = 9, column = 3, rowspan = 5, columnspan= 1, padx = 5, pady = 5)

output_text = tkst.ScrolledText(frame_SE, wrap = tk.WORD, width = 55, height = 10, undo = False)
output_text['font'] = ('consolas', '10')
output_text.insert(tk.INSERT, str(output))
output_text.pack(expand=True, anchor = 'w')

frame_W = tk.LabelFrame(root, width = 40, padx = 5, pady = 5, height = 100)
frame_W.grid(row = 4, column = 0, rowspan = 2, columnspan = 1, padx = 10, pady = 10, sticky = 'w')
frame_C1 = tk.LabelFrame(root, width = 70, padx = 5, pady = 5, height = 100)
frame_C1.grid(row = 4, column = 2, rowspan = 2, padx = 5, pady = 5, sticky = 'e')

frame_C2 = tk.LabelFrame(root, width = 70, padx = 5, pady = 5, height = 100)
frame_C2.grid(row = 6, column = 2, rowspan = 2, padx = 5, pady = 5, sticky = 'e')

detect_method = tk.StringVar()
auto_manual = 'auto'
detect_method.set('auto detect')

tk.Radiobutton(frame_W, text = "MANUAL DETECT - Manually draw circles to get diameter values", 
	variable = detect_method, value = 'manual detect', command = lambda:rd_button_clicked('manual')).pack(anchor = 'w')
tk.Radiobutton(frame_W, text = "AUTO DETECT - Uses 'Circle Hough Transform' to detect circles", 
	variable = detect_method, value = 'auto detect', command = lambda:rd_button_clicked('auto')).pack(anchor = 'w')

def rd_button_clicked(value):
	global auto_manual
	if value == 'auto':	
		auto_manual = value
		print(auto_manual + ", inside rd_button funct1")
	else:	
		auto_manual = value
		print(auto_manual + ", inside rd_button funct2")


frame_HoughCircle = tk.LabelFrame(root, text = 'Hough Circle Parameters', width = 70, padx = 5, pady = 5, height = 100)
frame_HoughCircle.grid(row = 6, column = 0, rowspan = 2, columnspan = 1, padx = 5, pady = 5)

param_minDist = tk.Entry(frame_HoughCircle, width = 5)
param_minDist.grid(row=0, column = 1, padx = 1, pady = 1)
label_minDist = tk.Label(frame_HoughCircle, text='Min Distance:')
label_minDist.grid(row=0,column=0, padx = 1, pady = 1)

param_dp = tk.Entry(frame_HoughCircle, width = 5)
param_dp.grid(row=1, column = 1, padx = 1, pady = 1)
label_dp = tk.Label(frame_HoughCircle, text='Accum/Res Ratio (dp):')
label_dp.grid(row=1,column=0, padx = 1, pady = 1)

param_minR = tk.Entry(frame_HoughCircle, width = 5)
param_minR.grid(row=0, column = 3, padx = 1, pady = 1)
label_minR = tk.Label(frame_HoughCircle, text=' Min Radius:')
label_minR.grid(row=0,column=2, padx = 1, pady = 1)

param_maxR = tk.Entry(frame_HoughCircle, width = 5)
param_maxR.grid(row=1, column = 3, padx = 1, pady = 1)
label_maxR = tk.Label(frame_HoughCircle, text=' Max Radius:')
label_maxR.grid(row=1,column=2, padx = 1, pady = 1)

param_p1 = tk.Entry(frame_HoughCircle, width = 5)
param_p1.grid(row=0, column = 5, padx = 1, pady = 1)
label_p1 = tk.Label(frame_HoughCircle, text=' Param1:')
label_p1.grid(row=0,column=4, padx = 1, pady = 1)

param_p2 = tk.Entry(frame_HoughCircle, width = 5)
param_p2.grid(row=1, column = 5, padx = 1, pady = 1)
label_p2 = tk.Label(frame_HoughCircle, text=' Param2:')
label_p2.grid(row=1,column=4, padx = 1, pady = 1)




frame_SW = tk.LabelFrame(root, width = 70)
frame_SW.grid(row=8, column = 0, rowspan = 5, columnspan = 3, padx = 5, pady = 5)


smaller_histo_img = ImageTk.PhotoImage(Image.open(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\black350.png'))
new_img_histo = tk.Label(frame_SW,image = smaller_histo_img)
new_img_histo.pack()

frame_NE = tk.LabelFrame(root, fg = 'black')
frame_NE.grid(row=0, column = 3, rowspan = 9, columnspan = 3, padx = 5, pady = 5)
frame_E = tk.LabelFrame(root, width = 60)
frame_E.grid(row=9, column = 5, columnspan = 1)


black_img = Image.open(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\RyLu_python_projects\Emulsion_openCV\black_bg.png')
width, height = black_img.size
max_wh = max(width, height)
factor = max_wh/600
black_img = black_img.resize((int(width/factor), int(height/factor)))
temp_img = ImageTk.PhotoImage(black_img)
placeholder_img = tk.Label(frame_NE, image = temp_img).pack()

def open_file():
	global my_img, window_img, placeholder_img, filename, show_img
	temp_img = Image.open(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\RyLu_python_projects\Emulsion_openCV\black_bg.png')
	black_img = ImageTk.PhotoImage(temp_img)
	background_img = tk.Label(frame_NE, image = black_img).place(x=0, y=0)

	filename = filedialog.askopenfilename(initialdir = r"C:\Users\ry129\Dropbox", title = "Select a file", filetypes = (("jpg Files", "*jpg"),("tiff Files", "*tiff")))
	my_img = Image.open(filename)
	width, height = my_img.size
	print(width, height)
	
	max_wh = max(width, height)
	factor = max_wh/600
	print(factor)
	my_img = my_img.resize((int(width/factor), int(height/factor)))
	adj_height = (600-(height/factor))/2
	print(adj_height)
	window_img = ImageTk.PhotoImage(my_img)
	show_img = tk.Label(frame_NE, image = window_img).place(x=0, y=adj_height)
	print(auto_manual + ", inside open_file funct1")


def start_state():
	global filename, temp_img, detected_img, output, smaller_histo_img, new_img_histo
	start_circle = True

	if auto_manual == 'auto' and start_circle == True:
		print(auto_manual + ", inside open_file funct2")
		output = adc.autoDetect(filename)
		temp_img = Image.open(filename.replace('.jpg', '_detected.jpg'))
		width, height = temp_img.size
		print(width, height)
		
		max_wh = max(width, height)
		factor = max_wh/600
		print(factor)
		temp_img = temp_img.resize((int(width/factor), int(height/factor)))
		adj_height = (600-(height/factor))/2
		print(adj_height)

		detected_img = ImageTk.PhotoImage(temp_img)
		new_img = tk.Label(frame_NE, image = detected_img).place(x=0, y=adj_height)

		output_text.insert(tk.INSERT, str(output) + '\n\n')

	if auto_manual == 'auto':
		histo_img = Image.open(filename.replace('.jpg', '_histogram.png'))
		width_histo, height_histo = histo_img.size
		max_wh = max(width_histo, height_histo)
		factor_histo = max_wh/350
		histo_temp_img = histo_img.resize((int(width_histo/factor_histo), int(height_histo/factor_histo)))

		smaller_histo_img = ImageTk.PhotoImage(histo_temp_img)
		new_img_histo = tk.Label(frame_SW, image = smaller_histo_img).place(x=0,y=0)


def clear_histo():
	global smaller_histo_img, new_img_histo
	adc.clear_plt()
	smaller_histo_img = ImageTk.PhotoImage(Image.open(r'C:\Users\ry129\Dropbox\1 - JHU M.S. Comp Sci courses\Projects_Python\black350.png'))
	new_img_histo = tk.Label(frame_SW,image = smaller_histo_img)
	new_img_histo.place(x=0, y=0)

img_button = tk.Button(frame_E, text = 'CLICK\nto upload an image', relief = 'raised', command = open_file)
img_button.config(height = 2, width = 19, font =('Helvetica', '10'))
img_button.pack()

start_button = tk.Button(frame_C1, text = 'START\nAuto/Manual Mode', relief = 'raised', command = start_state)
start_button.config(height = 2, width = 15, font =('Helvetica', '10'))
start_button.pack()
other_button = tk.Button(frame_C2, text = 'CLEAR\nHistogram', relief = 'raised', command = clear_histo)
other_button.config(height = 2, width = 15, font =('Helvetica', '10'))
other_button.pack()

credit = tk.Label(root, text = 'R.Lu (v1.0.0), 2020', font ='consolas 10 bold')
credit.grid(row=13, column = 5, sticky ='se')




root.mainloop()












