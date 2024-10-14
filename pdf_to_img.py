import fitz
import os

def parse_pdf(pdf_file):
    try:
        output_image_folder = "C:/New folder/Project/Project/PDF_to_IMG"

        # Delete existing images in folder
        for file_ in os.listdir(output_image_folder):
            try:
                file_path = f'{output_image_folder}/{file_}'
                os.remove(file_path)
            except:
                pass
        pdf_document = fitz.open(pdf_file)
        file_name = pdf_file.split('/')[-1].replace('.pdf','')
        # Iterate through each page and save it as an image
        for page_number in range(len(pdf_document)):
            output_img = f'{output_image_folder}/{file_name}~{page_number}.png'
            page = pdf_document.load_page(page_number)
            # You can adjust the DPI to control the resolution of the image
            image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
            
            image.save(output_img)

        pdf_document.close()
        print(f"{pdf_file} - PDF converted into Images...")
        print(output_image_folder)
        return os.listdir(output_image_folder)
    except Exception as e:
        print(f'Error -', e)