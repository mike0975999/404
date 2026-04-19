from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int
    chapter_number: int
    title: str
    author: str
    course: str
    year_level: int
    subject: str
    description: str
    pdf_url: str
    cover_url: str
    source: str