import fitz
pdf = fitz.open('examaple.pdf')
page = pdf.loadPage(2)
#print(page.rect.width*2)
image = page.get_pixmap(dpi=300)
image.save('output.png')