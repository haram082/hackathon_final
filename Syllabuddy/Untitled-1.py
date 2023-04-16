import pytesseract as pyt
import PIL as pil
import os
from pdf2image import convert_from_path

def file_to_txt(filename):
    """
    Reads an image uploaded and creates a txt file based off of it

    param: filename
    return: NO RETURN BUT DOES CREATE A TXT FILE
    """
    # Creates a txt file where we will write our information
    file_out = open('txt_file', "w")

    for pages in image_names:
        # Relative path so anyone can open and use this code without installing 
        pyt.pytesseract.tesseract_cmd = os.path.join('tesseract', 'tesseract.exe')

        # variable that gets all the text it read from an image
        img_to_string = pyt.image_to_string(pages)
        print(img_to_string)
        
        # writes all of the string into a txt file and adds a line at the end
        file_out.write(img_to_string)
        file_out.write("\n")

        
    file_out.close()

def pdf_to_png(pdf_name):
    """
    makes pdf into multiple images and gives us the name of them through a list

    param: name of the file
    """
    img_list = []
    # Relative path so anyone can open and use this code without installing 
    poppler_path = os.path.join('poppler', 'bin')

    # converts pdf pages into images and saves the number of pages
    pages = convert_from_path(pdf_name, poppler_path=poppler_path)
    
    # saves each page of the PDF as a PNG file with a specific name
    for i, page in enumerate(pages):
        page.save(f"page{i+1}.png", 'PNG')
        img_list.append(f"page{i+1}.png")

    # returns a list with the names
    return img_list

def string_to_txt_file(paragraph):
    file_out = open("txt_file2", 'w')
    file_out.write(paragraph)

image_names = pdf_to_png("Syllabus-ECON.pdf")
file_to_txt(image_names)




    
