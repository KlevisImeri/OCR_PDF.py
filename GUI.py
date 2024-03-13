
from tkinter import *
from tkinter import filedialog 

#GUI

#functions for buttons
def openFile():
	global filepath
	filepath = filedialog.askopenfilename()
	global label1
	label1 = Label(window, bg='#202124',fg='#d6d6d7', text = filepath,font=('Product Sans', 20) )
	label1.place(x=230, y=30)

def convertedFile():
	global folderpath
	folderpath = filedialog.askdirectory()
	global label2
	label2 = Label(window, bg='#202124',fg='#d6d6d7', text = folderpath, font=('Product Sans', 20))
	label2.place(x=230, y=90)

def exitKlevis():
    global dpiuser
    dpiuser = int(dropMeny.get())
    global convertedName
    convertedName = entry.get()
    window.destroy()



#Main window
window = Tk()
txtfileon = IntVar()
docxfileon = IntVar()
window.geometry("800x340")
window.configure(bg='#202124')
window.title("PDF->Redable PDF  CONVERTER")

#Asking the filedirectory and where to save 
button1 = Button(bg='#a4ade9', fg='#202124',borderwidth=0, text=' Open the file ', font=('Product Sans', 20), command=openFile)
button2 = Button(bg='#a4ade9', fg='#202124',borderwidth=0, text=' Save the file ',font=('Product Sans', 20), command=convertedFile)
button3 = Button(bg='#ff6666', fg='#202124',borderwidth=0, text = '       RUN       ', font=('Product Sans', 20), command=exitKlevis)
button1.place(x=20, y=20)
button2.place(x=20, y=80)
button3.place(x=600, y=260)

#to get the convertedname
entry = Entry(window, bg='#4c4c4c', fg='#d6d6d7', borderwidth=0, font=('Product Sans', 20))
entry.place(x=487, y=140)
label3 = Label(window, bg='#202124', fg='#d6d6d7', text="What would you like to name the file?",font=('Product Sans', 20))
label3.place(x=20, y=140)

#checkWORDorTXT
check_txt = Checkbutton(window,bg='#202124',fg='#d6d6d7', text="add convert to txt", font=('Product Sans', 20), variable=txtfileon , onvalue=1, offvalue=0,)
check_docx = Checkbutton(window,bg='#202124', fg='#d6d6d7',text="add convert to docx",font=('Product Sans', 20), variable=docxfileon , onvalue=1, offvalue=0,)
check_txt.place(x=20, y=200)
check_docx.place(x=20, y=260)

#comboBoxDpi
label4 = Label(window, bg='#202124', fg='#d6d6d7', text = 'DPI', font=('Product Sans', 20))
label4.place(x=403,y=200)
options=[300,350,400,450,500,600,800]
dropMeny = StringVar()
dropMeny.set(options[1])
comboBox = OptionMenu(window, dropMeny, *options)
comboBox.place(x=380,y=240)
comboBox.config(bg='#a4ade9', fg='#202124',borderwidth=0,font=('Product Sans', 25), highlightbackground='#a4ade9')
window.mainloop()

print(filepath)
print(folderpath)
print(convertedName)
print(dpiuser)
