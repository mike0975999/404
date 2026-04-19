import os
import json
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.pdf_utils import extract_text_from_pdf_url

load_dotenv()

router = APIRouter()

OPENROUTER_API_KEY = os.getenv("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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class QuizRequest(BaseModel):
    title: str
    author: str
    pdf_url: str

@router.post("/generate-quiz")
def generate_quiz(payload: QuizRequest):
    if not payload.pdf_url.strip():
        raise HTTPException(status_code=400, detail="This book has no PDF URL.")

    try:
        content_text = extract_text_from_pdf_url(payload.pdf_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract PDF text: {str(e)}")

    if not content_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in PDF.")

    return generate_ai_quiz_from_text(
        title=payload.title,
        author=payload.author,
        content_text=content_text[:20000]
    )