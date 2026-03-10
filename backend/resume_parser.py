import pdfplumber
import docx
import re
import warnings
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


def extract_text(file_path):

    text = ""

    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        print("⚠ PDF extraction warning:", e)
        return ""

    return clean_text(text)


def clean_text(text):
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.lower()
    return text.strip()