import PyPDF2
import re
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for i in range(reader.numPages):
            page = reader.getPage(i)
            text += page.extractText()
    return text

