import fitz
import requests
import tempfile
import os

def extract_text_from_pdf_url(pdf_url: str) -> str:
    if not pdf_url:
        return ""

    response = requests.get(pdf_url, timeout=30)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    text = ""
    try:
        doc = fitz.open(tmp_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return text[:20000]