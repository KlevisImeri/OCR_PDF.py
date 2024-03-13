import os			    # for directory managing
from tkinter import *
from tkinter import filedialog   #to create filepath and GUI
from PyPDF2 import PdfFileMerger
from pdf2image import convert_from_path
from pdf2docx import Converter, parse
import shutil
import tempfile

#setting temporay envrironment paths
popplerPath = os.getcwd()+'/poppler/bin'
tesseractPath = os.getcwd()+'/Tesseract-OCR'
os.environ["PATH"] += os.pathsep + os.pathsep.join([popplerPath])
os.environ["PATH"] += os.pathsep + os.pathsep.join([tesseractPath])
print(os.environ["PATH"])


#get file paths
def openFile():
	global filepath
	filepath = filedialog.askopenfilename()
	global label1
	label1 = Label(window, text = filepath, relief=SUNKEN, bd=2)
	label1.place(x=140, y=10)

def convertedFile():
	global folderpath
	folderpath = filedialog.askdirectory()
	global label2
	label2 = Label(window, text = folderpath, relief=SUNKEN, bd=2)
	label2.place(x=140, y=40)

def exitKlevis():
	global convertedName
	convertedName = entry.get()
	window.destroy()

#GUI
window = Tk()
txtfileon = IntVar()
docxfileon = IntVar()
window.geometry("600x200")
window.title("PDF->Redable PDF  CONVERTER")
button1 = Button(text='      Open the file        ' , command=openFile)
button2 = Button(text='      Where to save      ', command=convertedFile)
button3 = Button(text = 'RUN', command=exitKlevis)
button1.place(x=10, y=10)
button2.place(x=10, y=40)
button3.place(x=50, y=160)
entry = Entry(window)
entry.place(x=10, y=70)
label3 = Label(window, text="Put the name you like of the converted file without . , / ; : or any other weird symbol",relief=SUNKEN, bd=1)
label3.place(x=140, y=70)
check_txt = Checkbutton(window,text="add convert to txt", variable=txtfileon , onvalue=1, offvalue=0,)
check_docx = Checkbutton(window,text="add convert to docx", variable=docxfileon , onvalue=1, offvalue=0,)
check_txt.place(x=10, y=100)
check_docx.place(x=10, y=130)
window.mainloop()

# Create a temporal directory to store the pngs and the one-page converted pdf
where_to_save = folderpath
tempDir = tempfile.mkdtemp()
print(tempDir)

# convert PDF to PNG(s) and then to redable PDF or TEXT
textlist = []
merger = PdfFileMerger()
images = convert_from_path(filepath)
for i, image in enumerate(images):
	image.save(tempDir+f'/save_{i}.png')
	print(tempDir+f'/save_{i}.png')
	combined_pic = tempDir+f'/save_{i}.png'
	combined_saved =  tempDir+f'/save_{i}'
	print(combined_pic)
	tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" -l sqi+eng+srp_latn PDF' 
	print(tesseract)
	os.system(tesseract)
	if (txtfileon.get()==1):
		tesseract = 'tesseract "' + combined_pic + '" "' + combined_saved + '-ocr" -l sqi+eng+srp_latn txt' 
		print(tesseract)
		os.system(tesseract)
		textlist.append(combined_saved +'-ocr.txt')
	merger.append(tempDir+f'/save_{i}.png-ocr.pdf')
	print(tempDir+f'/save_{i}.png-ocr.pdf') 	
merger.write( convertedName +'.pdf')
merger.close()
print(merger)

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
print('temperory folder removed')

print("[[[[[[[[[[[[[[[[[[[ P R O C E S I    K A    P E R F U N D U A R]]]]]]]]]]]]]]]]]]]]]]]]")
