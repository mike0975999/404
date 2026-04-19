from sqlmodel import Session
from app.database import engine
from app.models import Book

def seed_books():
    books = [
        Book(
            title="Introduction to Programming",
            author="John Zelle",
            course="CS",
            year_level=1,
            subject="Programming Fundamentals",
            description="Introductory programming book",
            pdf_url="https://example.com/intro_programming.pdf",
            cover_url="https://example.com/intro_programming.jpg",
            source="manual"
        ),
        Book(
            title="Data Structures and Algorithms",
            author="Mark Allen Weiss",
            course="CS",
            year_level=2,
            subject="Data Structures",
            description="Core data structures book",
            pdf_url="https://example.com/dsa.pdf",
            cover_url="https://example.com/dsa.jpg",
            source="manual"
        ),
        Book(
            title="Computer Networking",
            author="Andrew S. Tanenbaum",
            course="IT",
            year_level=2,
            subject="Networking",
            description="Networking fundamentals",
            pdf_url="https://example.com/networking.pdf",
            cover_url="https://example.com/networking.jpg",
            source="manual"
        )
    ]

    with Session(engine) as session:
        for book in books:
            session.add(book)
        session.commit()

if __name__ == "__main__":
    seed_books()