from sqlmodel import Session, select
from app.database import engine
from app.models import Book

def seed_books():
    books = [
        Book(
            title="Open Data Structures",
            author="Pat Morin",
            course="CS",
            year_level=2,
            subject="Algorithms & Data Structures",
            description="Covers arrays, linked lists, trees, graphs, sorting.",
            pdf_url="https://opendatastructures.org/ods-python.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Algorithms",
            author="Jeff Erickson",
            course="CS",
            year_level=2,
            subject="Algorithms & Data Structures",
            description="Detailed full algorithms textbook.",
            pdf_url="https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Discrete Mathematics: An Open Introduction",
            author="Oscar Levin",
            course="CS",
            year_level=2,
            subject="Discrete Math & Theory",
            description="Logic, proofs, combinatorics, graphs.",
            pdf_url="https://discrete.openmathbooks.org/pdfs/dmoi-tablet.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Operating Systems: Three Easy Pieces",
            author="Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau",
            course="CS",
            year_level=2,
            subject="Operating Systems",
            description="Processes, memory, concurrency.",
            pdf_url="https://pages.cs.wisc.edu/~remzi/OSTEP/ostep.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Database Design",
            author="Adrienne Watt and Nelson Eng",
            course="CS",
            year_level=2,
            subject="Databases",
            description="SQL, relational design, normalization.",
            pdf_url="https://opentextbc.ca/dbdesign01/open/download?type=pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Computer Networking: Principles, Protocols and Practice",
            author="Olivier Bonaventure",
            course="CS",
            year_level=2,
            subject="Computer Networks",
            description="Networking fundamentals, TCP/IP, protocols.",
            pdf_url="https://inl.info.ucl.ac.be/system/files/CNP3.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Think Python (2nd Edition)",
            author="Allen Downey",
            course="CS",
            year_level=2,
            subject="Programming / Software Engineering",
            description="Programming foundations using Python.",
            pdf_url="https://greenteapress.com/thinkpython2/thinkpython2.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Software Engineering",
            author="Ian Sommerville",
            course="CS",
            year_level=2,
            subject="Programming / Software Engineering",
            description="Software engineering reference material.",
            pdf_url="",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="Think Stats",
            author="Allen Downey",
            course="CS",
            year_level=2,
            subject="Data Science / Analytics",
            description="Statistics and data analysis using Python.",
            pdf_url="https://greenteapress.com/thinkstats2/thinkstats2.pdf",
            cover_url="",
            source="custom_pdf"
        ),
        Book(
            title="An Introduction to Statistical Learning",
            author="Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani",
            course="CS",
            year_level=2,
            subject="Data Science / Analytics",
            description="Machine learning and analytics fundamentals.",
            pdf_url="https://www.statlearning.com/s/ISLR-Seventh-Printing.pdf",
            cover_url="",
            source="custom_pdf"
        )
    ]

    with Session(engine) as session:
        existing_books = session.exec(select(Book)).all()
        for old_book in existing_books:
            session.delete(old_book)
        session.commit()

        for book in books:
            session.add(book)
        session.commit()

if __name__ == "__main__":
    seed_books()