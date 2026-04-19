import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

DATABASE_URL = "sqlite:///./test.db"
print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)