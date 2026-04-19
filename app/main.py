from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes.books import router as books_router
from app.routes.quiz import router as quiz_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(books_router)
app.include_router(quiz_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}