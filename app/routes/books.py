from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.database import engine
from app.models import Book, Chapter
from app.chapter_utils import extract_text_from_pdf_url, split_into_chapters
from app.seed import seed_books

router = APIRouter()


@router.get("/books")
def get_books(course: str = Query(...), year_level: int = Query(...)):
    with Session(engine) as session:
        statement = select(Book).where(
            Book.course == course,
            Book.year_level == year_level
        )
        books = session.exec(statement).all()

        return [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "course": b.course,
                "year_level": b.year_level,
                "subject": b.subject,
                "description": b.description,
                "pdf_url": b.pdf_url,
                "cover_url": b.cover_url,
                "source": b.source
            }
            for b in books
        ]


@router.post("/books/{book_id}/generate-chapters")
def generate_chapters(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)

        if not book or not book.pdf_url:
            return {"error": "Book or PDF missing"}

        old_chapters = session.exec(
            select(Chapter).where(Chapter.book_id == book_id)
        ).all()

        for old in old_chapters:
            session.delete(old)

        text = extract_text_from_pdf_url(book.pdf_url)
        chapters = split_into_chapters(text)

        for ch in chapters:
            session.add(
                Chapter(
                    book_id=book_id,
                    chapter_number=ch["chapter_number"],
                    title=ch["title"],
                    content=ch["content"]
                )
            )

        session.commit()
        return {"generated": len(chapters)}


@router.get("/books/{book_id}/chapters")
def get_chapters(book_id: int):
    with Session(engine) as session:
        chapters = session.exec(
            select(Chapter)
            .where(Chapter.book_id == book_id)
            .order_by(Chapter.chapter_number)
        ).all()
        return chapters


@router.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: int):
    with Session(engine) as session:
        chapter = session.get(Chapter, chapter_id)
        if not chapter:
            return {"error": "Chapter not found"}
        return chapter
    
@router.post("/admin/seed-books")
def seed_books_route():
    seed_books()
    return {"message": "books seeded"}