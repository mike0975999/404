from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.database import engine
from app.models import Book
import requests

router = APIRouter()

OPEN_LIBRARY_SUBJECTS = {
    ("CS", 1): "computer_science",
    ("CS", 2): "data_structures",
    ("CS", 3): "algorithms",
    ("CS", 4): "artificial_intelligence",

    ("IT", 1): "information_technology",
    ("IT", 2): "networking",
    ("IT", 3): "databases",
    ("IT", 4): "cyber_security",

    ("EMC", 1): "multimedia",
    ("EMC", 2): "graphic_design",
    ("EMC", 3): "game_design",
    ("EMC", 4): "interactive_multimedia",

    ("ACT", 1): "computer_literacy",
    ("ACT", 2): "programming",
    ("ACT", 3): "information_technology",
    ("ACT", 4): "computer_science"
}

def fetch_openlibrary_books(course: str, year_level: int):
    subject = OPEN_LIBRARY_SUBJECTS.get((course.upper(), year_level), "computer_science")
    url = f"https://openlibrary.org/subjects/{subject}.json?limit=10"
    print("FETCHING OPEN LIBRARY:", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        books = []
        for index, work in enumerate(data.get("works", []), start=1000):
            title = work.get("title", "Untitled")
            authors = work.get("authors", [])
            author_name = authors[0]["name"] if authors else "Unknown Author"
            cover_id = work.get("cover_id")

            cover_url = (
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                if cover_id else ""
            )

            books.append({
                "id": index,
                "title": title,
                "author": author_name,
                "course": course,
                "year_level": year_level,
                "subject": subject.replace("_", " ").title(),
                "description": f"Open Library book for {course} year {year_level}",
                "pdf_url": "",
                "cover_url": cover_url,
                "source": "openlibrary"
            })
        return books
    except Exception as e:
        print("Open Library fetch failed:", e)
        return []

@router.get("/books")
def get_books(course: str = Query(...), year_level: int = Query(...)):
    db_books = []
    with Session(engine) as session:
        statement = select(Book).where(
            Book.course == course,
            Book.year_level == year_level
        )
        db_books = session.exec(statement).all()

    online_books = fetch_openlibrary_books(course, year_level)

    db_books_as_dict = [
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
        for b in db_books
    ]

    return db_books_as_dict + online_books