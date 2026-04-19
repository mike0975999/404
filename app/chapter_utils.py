import fitz
import requests
import re
import tempfile

def extract_text_from_pdf_url(pdf_url: str):
    response = requests.get(pdf_url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(response.content)
        path = f.name

    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()

    return text

def split_into_chapters(text: str):
    pattern = r"(Chapter\s+\d+.*?)(?=Chapter\s+\d+|$)"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

    chapters = []

    if not matches:
        # fallback if no chapters detected
        size = 5000
        for i in range(0, len(text), size):
            chapters.append({
                "chapter_number": len(chapters)+1,
                "title": f"Section {len(chapters)+1}",
                "content": text[i:i+size]
            })
        return chapters

    for i, chunk in enumerate(matches, start=1):
        lines = chunk.strip().splitlines()
        title = lines[0] if lines else f"Chapter {i}"
        content = "\n".join(lines[1:])

        chapters.append({
            "chapter_number": i,
            "title": title,
            "content": content
        })

    return chapters