
# Importing required modules
from pypdf import PdfReader
import os

def main():
    # Specify the path to the PDF file
    pdf_path = 'C:/Users/USER/Desktop/Presentatio Tech/Collecting techniques/Inputs/w.pdf'
    output_txt_path = 'C:/Users/USER/Desktop/Presentatio Tech/Collecting techniques/Onputs/extracted_text.txt'

    try:
        # Creating a PDF reader object
        reader = PdfReader(pdf_path)

        # Printing number of pages in the PDF file
        num_pages = len(reader.pages)
        print(f'Number of pages: {num_pages}')

        # Getting a specific page from the PDF file
        page = reader.pages[0]

        # Extracting text from the page
        text = page.extract_text()

        if text:
            print(text)

            # Saving the extracted text to a text file
            with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            print(f'Text extracted and saved to {output_txt_path}')
        else:
            print('No text found on the specified page.')

    except FileNotFoundError:
        print(f'Error: The file {pdf_path} was not found.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
