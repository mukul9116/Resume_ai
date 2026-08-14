import io
import pdfplumber
import docx

class ExtractionError(Exception):
    pass

def extract_text_from_pdf(file_bytes:bytes) -> str:
    pass   # extraction of text from pdf

def extract_text_from_docx(file_bytes:bytes) -> str:
    pass   # extraction of text from docx

def extract_text_from_resume(file_bytes:bytes) -> str:
    pass  # here i will write code for checking file extension