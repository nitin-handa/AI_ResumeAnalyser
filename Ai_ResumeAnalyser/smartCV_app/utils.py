# import os

# def get_pdf_text(file_path):
#     # Normalize the file path
#     file_path = os.path.normpath(file_path)
    
#     # Check if file exists
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError(f"No such file: '{file_path}'")
    
#     # Extract text from PDF (example, you need to use your own function/method)
#     text = extract_text_from_pdf(file_path)  # Replace with your actual text extraction function
#     return text
import os
from pdfminer.high_level import extract_text as pdfminer_extract_text
from docx import Document

def extract_text_from_file(file_path):
    # Normalize the file path
    file_path = os.path.normpath(file_path)
    
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    
    # Determine file type and extract text accordingly
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        return extract_text_from_docx(file_path)
    elif file_ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f'Unsupported file type: {file_ext}')

def extract_text_from_pdf(pdf_path):
    try:
        return pdfminer_extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error extracting text from DOCX '{docx_path}': {e}")
        return ""

def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from TXT '{txt_path}': {e}")
        return ""