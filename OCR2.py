import os			    # for directory managing
from tkinter import *
from tkinter import filedialog   #to create filepath and GUI
from PyPDF2 import PdfFileMerger
from pdf2docx import Converter, parse
import shutil
import tempfile
import fitz

#setting temporay envrironment paths 
# this is only if you have tessaract localy and for the output of sefl sufficent exe
# if you have installed tessaract globally you dont need it.
# tesseractPath = os.getcwd()+'/Tesseract-OCR'
# os.environ["PATH"] += os.pathsep + os.pathsep.join([tesseractPath])
print('[[[[[[[[[[[[[[[[[[[ P R O G R A M I    K A    F I L L U A R]]]]]]]]]]]]]]]]]]]]]]]]')

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

#Dependiceis of the core--------------------------------------------------

# Create a temporal directory to store the pngs and the one-page converted pdf
where_to_save = folderpath
tempDir = tempfile.mkdtemp()
print(tempDir)

# we need this to create text file
textlist = []
# we need this to iniciate the filemerger
merger = PdfFileMerger()

# open pdf for fitz(mupypdf) and get page count
pdf = fitz.open(filepath)
pageCount= pdf.pageCount
print(pageCount)

# the core of the program----------------------------------------------------
for i in range(pageCount):

	# converion pdf to image using fitz
	page = pdf.loadPage(i)
	image = page.getPixmap(dpi=dpiuser)
	image.save(tempDir+f'/save_{i}.png')
	#print(f'save_{i}.png'+' - image was created')

	# Tessaract OCR images converion 
	combined_pic = tempDir+f'/save_{i}.png'
	combined_saved =  tempDir+f'/save_{i}'
	tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" -l sqi+eng+srp_latn PDF' 
	#print(f'save_{i}.png'+' - image was scanned to PDF')
	os.system(tesseract)
	if (txtfileon.get()==1):
		tesseract = 'tesseract "' + combined_pic + '" "' + combined_saved + '-ocr" -l sqi+eng+srp_latn txt' 
		#print(f'save_{i}.png'+' - image was scanned to TEXT')
		os.system(tesseract)
		textlist.append(combined_saved +'-ocr.txt')
	merger.append(tempDir+f'/save_{i}.png-ocr.pdf')	
	#print(f'save_{i}.png'+' - appendit to merger')
	print(f'Page_[{i}] - finished')
merger.write( convertedName +'.pdf')
merger.close()
print('The PDF created')

with open(convertedName+'_TXT.txt','wb') as wfd:
    for f in textlist:
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd)

# merging and moving txt(s)

#with open(convertedName+'_TXT.txt', 'w') as outfile:
 #     with open(names) as infile:
   #         outfile.write(infile.read())
   #     outfile.write("\n")

if (txtfileon.get()==1):	
	shutil.move(convertedName+'_TXT.txt', where_to_save)
else:
	os.remove(convertedName+'_TXT.txt')

# CONVERSION TO DOCX------------------------------------------------------------------------------------------------------
if (docxfileon.get()==1):
	pdf_file = convertedName +'.pdf'
	word_file = convertedName+'_WORD.docx'


	# Convertor Method
	cv = Converter(pdf_file)
	cv.convert(word_file, start=0, end=None)
	cv.close()

	#Parse Method
	#parse(pdf_file, word_file, start=0, end=None)
	shutil.move(convertedName+'_WORD.docx', where_to_save)
#------------------------------------------------------------------------------------------------------------------------

#sent completed files to desktop
shutil.move(convertedName+'.pdf', where_to_save)
print('File in:'+ where_to_save)

#delete temporory folder
shutil.rmtree(tempDir)
print('-------Temperory folder removed---------')

print("[[[[[[[[[[[[[[[[[[[ P R O C E S I    K A    P E R F U N D U A R]]]]]]]]]]]]]]]]]]]]]]]]")