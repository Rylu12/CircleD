import tkinter

root = tkinter.Tk()
root.call('tk', 'scaling', 2.0)

menubar = tkinter.Menu(root)
root.config(menu=menubar)

fileMenu = tkinter.Menu(menubar, tearoff=False)
editMenu = tkinter.Menu(menubar, tearoff=False)

menubar.add_cascade(label="File",underline=0, menu=fileMenu)
menubar.add_cascade(label="Edit",underline=0, menu=editMenu)

fileMenu.add_command(label="Open...", underline=0)
fileMenu.add_command(label="Save", underline=0)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", underline=1)

editMenu.add_command(label="Cut", underline=2)
editMenu.add_command(label="Copy", underline=0)
editMenu.add_command(label="Paste", underline=0)

root.mainloop()


